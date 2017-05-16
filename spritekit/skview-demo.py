import ui
from objc_util import CGRect, CGPoint, CGSize, ObjCClass, ObjCInstance, NSBundle

NSBundle.bundleWithPath_("/System/Library/Frameworks/SpriteKit.framework").load()
SKView = ObjCClass('SKView')
SKNode = ObjCClass('SKNode')


class MyView(ui.View):
  
  debug = True
  
  def __init__(self):
    # Setup SKView
    screen_size = ui.get_screen_size()
    rect = CGRect(
      CGPoint(0, 0),
      CGSize(screen_size[0], screen_size[1]))
    skview = SKView.alloc().initWithFrame_(rect)
    skview.showsFPS = self.debug
    skview.showsNodeCount = self.debug
    skview.showsPhysics = self.debug
    ObjCInstance(self).addSubview(skview)
    self.skview = skview

  def will_close(self):
    self.skview.paused = True


if __name__ == '__main__':
  view = MyView()
  view.present(hide_title_bar=True) 
