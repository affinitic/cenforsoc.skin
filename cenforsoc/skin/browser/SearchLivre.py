from zope.component import getUtility, getMultiAdapter
from Products.Five.browser import BrowserView
from z3c.json.interfaces import IJSONWriter


class SearchLivreAutoCompleteJSON(BrowserView):

    def __call__(self):
        searchString = self.request.form.get('name_startsWith')
        livreView = getMultiAdapter((self.context, self.request), name="gestionLivre")
        terms = periodiqueView.getLivreeByLeffeSearch(searchString)
        writer = getUtility(IJSONWriter)
        self.request.response.setHeader('content-type', 'application/json')
        return writer.write(terms)

    def render(self):
        pass
