from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Count

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

from auctions.models import Category


class Graph:
    """A class to create analytics using Plotly graphs."""
    def __init__(self,
                 title:str,
                 labels:list|tuple,
                 values:list|tuple,
                 name:str =None):
        self.title = title
        self.name = name
        self.labels = labels
        self.values = values

    def get_graph_html(self, fig):
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            title_text=self.title,
            title_x=0.5)
        graph:str = pio.to_html(fig, include_plotlyjs=True, full_html=True)
        return graph

    def make_bar_graph(self):
        fig = go.Figure(data=[
            go.Bar(x=self.labels, y=self.values, name=self.name)
        ])
        return self.get_graph_html(fig)

    def make_pie_graph(self):
        fig = go.Figure(data=[
            go.Pie(labels=self.labels, values=self.values,
                   name=self.name, hole=0.6,
                   textinfo='percent', hoverinfo='label+value')
        ])
        if self.name:
            fig.update_traces(hoverinfo='label+value+name')
        return self.get_graph_html(fig)


class CategoryAnalyticsView(ListView):
    model = Category
    template_name = 'graphs/category_analytics.html'
    context_object_name = 'cat_graph'

    def get_queryset(self):
        qs = self.model.objects.order_by(
            'name'
        ).annotate(listings_count=Count('listing'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        graphs = self.get_graph()
        context['bar'] = graphs['bar']
        context['pie'] = graphs['pie']
        return context

    def get_graph(self):
        title = 'Number of listings per category'
        categories = tuple(cat.name for cat in self.get_queryset())
        listings_count = tuple(cat.listings_count for cat in self.get_queryset())
        name = 'listings'
        graph = Graph(title, categories, listings_count, name)
        return {'bar': graph.make_bar_graph(), 'pie': graph.make_pie_graph()}
