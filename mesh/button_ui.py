import button_demo
import cb
import ui


class ButtonDisplayView(ui.View):
    def __init__(self):
        self.background_color = 'white'

        self.label = ui.Label()
        self.label.text = "Init"
        self.label.text_color = "black"
        self.label.font = ('<system>', 64)
        self.label.flex = 'LRTB'
        self.add_subview(self.label)

        self.mesh = button_demo.MeshManager()
        self.mesh.ready = self.ready
        self.mesh.press = self.press
        self.mesh.hold = self.hold
        self.mesh.double_press = self.double_press

        cb.set_central_delegate(self.mesh)
        cb.scan_for_peripherals()
    
    def ready(self):
        self.label.text = "Ready"
        self.label.text_color = "red"
        self.label.size_to_fit()
    
    def press(self):
        self.label.text = "Press"
        self.label.text_color = "black"
        self.label.size_to_fit()
        self.background_color = "white"

    def hold(self):
        self.label.text = "Hold"
        self.label.text_color = "red"
        self.label.size_to_fit()
        self.background_color = "orange"
        
    def double_press(self):
        self.label.text = "Double Press"
        self.label.text_color = "yellow"
        self.label.size_to_fit()
        self.background_color = "green"
                
    def will_close(self):
        self.mesh.die()
        cb.reset()


if __name__ == '__main__':
    view = ButtonDisplayView()
    view.present('fullscreen')
