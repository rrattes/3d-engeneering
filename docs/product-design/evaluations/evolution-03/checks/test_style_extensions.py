from helpers import LocalProject
from style_brief import make_brief
class StyleExtensions(LocalProject):
 def test_old_call(self):self.assertEqual(make_brief('minimalista')['style'],'minimalista')
 def test_optional_family(self):
  rules={'shared':['handle'],'vary':['front']};intent={'handle':{'action':'pull','constraint':'clearance'}}
  result=make_brief('minimalista',family_rules=rules,interaction_intent=intent)
  self.assertEqual(result['family_rules'],rules);self.assertEqual(result['interaction_intent'],intent)
 def test_custom_optional(self):self.assertEqual(make_brief('custom',custom={'form':'arc','criteria':['silhouette']},family_rules={'shared':['handle']})['family_rules']['shared'],['handle'])
 def test_bad_optional(self):
  with self.assertRaises(ValueError):make_brief('gamer',family_rules='force five')
