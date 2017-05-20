import ui
from objc_util import CGRect, CGPoint, CGSize, ObjCClass, ObjCInstance, NSBundle, create_objc_class

NSBundle.bundleWithPath_("/System/Library/Frameworks/SpriteKit.framework").load()
SKView = ObjCClass('SKView')
SKScene = ObjCClass('SKScene')
SKPhysicsBody = ObjCClass('SKPhysicsBody')
SKNode = ObjCClass('SKNode')


def DemoScene_touchesBegan_withEvent_(_self, _cmd, _touches, event):
  touches = ObjCInstance(_touches)
  print(touches)


DemoScene = create_objc_class(
  'DemoScene',
  SKScene,
  methods=[DemoScene_touchesBegan_withEvent_],
  protocols=[])


class MyView(ui.View):
  
  debug = True
  
  def __init__(self):
    # Setup SKView
    screen_size = ui.get_screen_size()
    rect = CGRect(
      CGPoint(0, 0),
      CGSize(screen_size[0], screen_size[1]))
    skview = SKView.alloc().initWithFrame_(rect)
    # debug
    skview.showsFPS = self.debug
    skview.showsNodeCount = self.debug
    skview.showsPhysics = self.debug
    ObjCInstance(self).addSubview(skview)
    self.skview = skview
    scene = DemoScene.sceneWithSize_(rect.size)
    skview.presentScene_(scene)
    self.scene = scene

  def will_close(self):
    self.skview.paused = True


if __name__ == '__main__':
  view = MyView()
  view.present(hide_title_bar=True) 
