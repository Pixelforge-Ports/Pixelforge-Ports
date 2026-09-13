import unittest
from github_catalog import choose_release

def release(tag,date,prerelease=False,draft=False,asset='Residual.zip'):
    return dict(tag_name=tag,published_at=date,prerelease=prerelease,draft=draft,
                assets=[dict(name=asset,state='uploaded')])

class Releases(unittest.TestCase):
    def test_new_prerelease_selected_and_label_preserved(self):
        stable=release('v1','2026-09-01');test=release('v2','2026-09-13',True)
        selected,asset=choose_release([stable,test],'residual.zip')
        self.assertEqual(selected['tag_name'],'v2')
        self.assertTrue(selected['prerelease'])
    def test_draft_and_unrelated_assets_are_not_downloads(self):
        draft=release('v3','2026-09-13',draft=True)
        other=release('v2','2026-09-12',asset='source.zip')
        self.assertEqual(choose_release([draft,other],'residual.zip'),(None,None))
    def test_old_matching_release_kept_until_new_zip_uploaded(self):
        old=release('v1','2026-09-01');new=release('v2','2026-09-13');new['assets'][0]['state']='new'
        self.assertEqual(choose_release([new,old],'residual.zip')[0]['tag_name'],'v1')
    def test_empty_releases_have_no_download(self):
        self.assertEqual(choose_release([],'residual.zip'),(None,None))

if __name__=='__main__':unittest.main()
