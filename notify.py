import ui
import console
import notification

def alert(sender):
  console.alert('alert1')
  
def push(sender):
  notification.schedule('push 1', 1)
  
def hud_alert(sender):
  console.hud_alert('hud alert1')
  
v = ui.load_view()
v.present('sheet')
