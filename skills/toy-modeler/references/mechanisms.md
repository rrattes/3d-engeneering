# Mechanisms as play

For each mechanism record: part, action/control point, motion or state change, response the player perceives, useful range/stop, and how the play resets. Add CAD dimensions and constraints in the engineering source of truth.

| Mechanism | Play roles | Prototype questions |
|---|---|---|
| Pin hinge/friction joint | Pose a character, open a compartment, fold or transform | Does it hold useful poses? Is repositioning satisfying? |
| Ball/socket or segmented joint | Aim a head, pose limbs, curve a tail | Can the player reach expressive configurations without frustration? |
| Wheel/axle/cam/gear | Travel, follow a path, reveal linked movement | Is the resulting motion visible and repeatable? |
| Snap/slide/connectors | Assemble, exchange accessories, transform | Are combinations understandable and worth repeating? |
| Detent/ratchet | Click through positions, count or sequence actions | Does sound/tactile feedback support the intended action? |
| Flexure/spring | Squeeze, bend, release, bounce in place | Is return perceptible and pleasant at intended scale? Measure force and cycles on a real print; CAD alone cannot predict feel or life. |

Reuse CAD3D's `pin_hinge` interface and `motion_paths` rotation checks where suitable. A modeled joint is not automatically retained, pose-holding, easy to operate, or pleasant. Record those as prototype questions rather than adding speculative geometry checks. Motors, batteries, magnets, and projectiles are outside the initial skill scope unless separately requested and assessed.
