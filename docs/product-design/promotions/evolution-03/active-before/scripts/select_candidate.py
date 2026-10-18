#!/usr/bin/env python3
"""Select within this workflow after actual user approval; never publish a CAD3D release."""
import argparse
import json
import os
import tempfile
from pathlib import Path
from evaluate_design import evaluate_design
from pd_common import artifact, canonical_sha, file_sha, load_json, local_path


def select_candidate(contract, candidate, project_root, review_ref, decision_ref):
    root = Path(project_root).resolve()
    result = {'selection': 'BLOCKED', 'physical_validation': 'NOT_EVALUATED'}
    lock = None
    temporary = None
    try:
        gate = evaluate_design(contract, candidate, root)
        result['engineering'] = gate
        if gate['eligibility'] != 'ELIGIBLE':
            raise ValueError('live engineering gate is not ELIGIBLE')
        review = artifact(root, review_ref, True)
        decision = artifact(root, decision_ref, True)
        binding = {'contract_sha256': canonical_sha(contract), 'candidate_sha256': canonical_sha(candidate)}
        if review.get('schema') != 'product-design-visual-review-v1' or review.get('status') != 'PASS':
            raise ValueError('complete visual review required')
        if review.get('revision') != candidate['revision'] or not isinstance(review.get('reviewer'), str) or not review['reviewer'].strip():
            raise ValueError('review revision and reviewer required')
        for key, value in binding.items():
            if review.get(key) != value or decision.get(key) != value:
                raise ValueError('review/decision binding mismatch')
        images = review.get('images')
        if not isinstance(images, list) or not images:
            raise ValueError('reviewed image references required')
        for image in images:
            artifact(root, image)
        image_paths = {ref['path'] for ref in images}
        expected = contract.get('visual_criteria')
        if not isinstance(expected, list) or not expected or any(not isinstance(x, str) or not x for x in expected) or len(set(expected)) != len(expected):
            raise ValueError('explicit visual criteria required for acceptance')
        criteria = review.get('criteria', [])
        if not isinstance(criteria, list) or len({x['id'] for x in criteria}) != len(criteria):
            raise ValueError('unique review criteria required')
        if any(item.get('status') != 'PASS' for item in criteria):
            raise ValueError('unclosed visual finding contradicts global PASS')
        indexed = {item['id']: item for item in criteria}
        for ident in expected:
            item = indexed.get(ident, {})
            if item.get('status') != 'PASS' or not item.get('finding') or not item.get('resolution'):
                raise ValueError('unclosed visual criterion: ' + ident)
            paths = item.get('image_paths')
            if not isinstance(paths, list) or not paths or not set(paths) <= image_paths:
                raise ValueError('criterion must reference reviewed images')
        if decision.get('authority') != 'user' or decision.get('decision') != 'APPROVED' or decision.get('target_scope') != contract['target_scope'] or decision.get('visual_review_sha256') != review_ref['sha256']:
            raise ValueError('current explicit user decision required')
        relative = 'design/product-design/accepted.json'
        pointer = root / relative
        if pointer.is_symlink() or pointer.parent.resolve() != pointer.parent:
            raise ValueError('selection pointer and parents must not be symlinks')
        pointer.parent.mkdir(parents=True, exist_ok=True)
        lock = pointer.with_suffix('.lock')
        # Exclusive lock coordinates this selector only, not external publishers.
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(descriptor)
        previous = file_sha(pointer) if pointer.exists() else None
        # Recheck records immediately before the atomic own-pointer write.
        if evaluate_design(contract, candidate, root)['eligibility'] != 'ELIGIBLE':
            raise ValueError('engineering evidence changed')
        artifact(root, review_ref); artifact(root, decision_ref)
        for image in images:
            artifact(root, image)
        payload = {'schema': 'product-design-selection-v1', 'revision': candidate['revision'],
                   'target_scope': contract['target_scope'], **binding, 'visual_review': review_ref,
                   'user_decision': decision_ref, 'physical_validation': 'NOT_EVALUATED'}
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=pointer.parent, prefix='.accepted-', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
        if (file_sha(pointer) if pointer.exists() else None) != previous:
            raise ValueError('accepted pointer changed concurrently')
        temporary.replace(pointer)
        result.update(selection='ACCEPTED', pointer=relative, target_scope=contract['target_scope'])
    except (ValueError, OSError, KeyError, TypeError, IndexError) as exc:
        result['reason'] = str(exc)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
        if lock is not None and 'descriptor' in locals():
            lock.unlink(missing_ok=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    for name in ('contract', 'candidate', 'visual-review', 'user-decision'):
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    try:
        def ref(name):
            return {'path': name, 'sha256': file_sha(local_path(args.project, name))}
        result = select_candidate(load_json(local_path(args.project, args.contract)),
                                  load_json(local_path(args.project, args.candidate)), args.project,
                                  ref(args.visual_review), ref(args.user_decision))
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0 if result['selection'] == 'ACCEPTED' else 3
    except (ValueError, OSError, TypeError) as exc:
        print('INVALID_INPUT: ' + str(exc)); return 2

if __name__ == '__main__':
    raise SystemExit(main())
