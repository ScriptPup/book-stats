import mplcyberpunk
import matplotlib.transforms as transforms
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from .chapter import Chapter
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.container import BarContainer

class Reports:
    def __init__(self, chapters: list[Chapter]):
        self.set_style()
        self.chapters: list[Chapter] = chapters
        

    def set_style(self, style_name: str = "cyberpunk"):
        plt.style.use(style_name)

    def words_by_chapter(self
                         , axes: Axes = None
                         , chart_type: str = "column"
                         , title: str = "Wordcount by Chapter"
                         , data_labels: bool = True
                         , data_label_options: dict = {"fmt": ",","offset": 0, "rotation": 0, "font_dict": {'weight' : 'bold','size': 10}}
                         , chart_args: dict = {}                         
                         ) -> tuple[Axes,list[Line2D]|BarContainer]:
        """
        :param chart_type: line, bar, column
        """       
        if not axes: axes = plt.gca() 
        data  = [chapt.stats.word_count for chapt in self.chapters]
        labels = [chapt.name for chapt in self.chapters]
        chart = self.plot_chart_type(axes, data, labels, chart_type=chart_type, **chart_args)
        self.set_title(axes,title)
        if data_labels:
            if chart_type in ["bars","columns"]:
                self.data_labels_bars(axes, chart, data, **data_label_options)        
        
        return axes,chart

    def plot_chart_type(self, axes: Axes, data: list[float|int], labels: list[str|datetime|int], chart_type: str = "column", **chart_args) -> list[Line2D]|BarContainer:
        if chart_type == "line":
            return axes.plot(labels,data,**chart_args)
        if chart_type == "column":
            return axes.bar(labels,data,**chart_args)
        if chart_type == "bar":
            return axes.barh(labels,data,**chart_args)
        
    def data_labels_bars(self
                         , axes: Axes
                         , bars: BarContainer
                         , labels: list[str]
                         , fmt=","
                         , offset=0
                         , rotation=0
                         , font_dict={'weight' : 'normal','size': 10}):
        i=0
        while i < len(bars) and labels:
            label = f"{labels[i]: {fmt}}"
            bar: Rectangle = bars[i]
            height = bar.get_height()
            axes.text((bar.get_x() + bar.get_width() / 2) - offset, height, f'{label}',
                    ha='center', va='bottom', fontdict=font_dict,rotation=rotation)
            i += 1

    def set_title(self, axes: Axes, title: str):
        axes.set_title(title)