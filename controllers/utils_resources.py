class ResourcesHandler(BaseHandler):
       """Handler for Resources page."""
       def get(self):
           """Handles GET requests."""
#           if not self.personalize_page_and_get_enrolled():
#               return
           
           self.template_value['navbar'] = {'resources': True}
           self.render('resources.html')
