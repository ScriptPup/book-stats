import mplcyberpunk
import matplotlib.transforms as transforms
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from wordcloud import WordCloud
from datetime import datetime
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from .chapter import Chapter
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.container import BarContainer

DEFAULT_CHART_OPTIONS = {"yaxis": True, "xaxis": True}

class Reports:
    def __init__(self, chapters: list[Chapter]):
        self.set_style()
        self.chapters: list[Chapter] = chapters
        

    def set_style(self, style_name: str = "cyberpunk"):
        try:
            plt.style.use(style_name)
        except:
            import warnings
            warnings.warn("Failed to apply cyberpunk style")

    def words_by_chapter(self
                         , axes: Axes = None
                         , chart_type: str = "column"
                         , title: str = "Wordcount by Chapter"
                         , data_labels: bool = False
                         , data_label_options: dict = {"fmt": ",","offset": 0, "rotation": 0, "font_dict": {'weight' : 'bold','size': 10}}
                         , xaxes_options: dict = { "rotation": 45 }
                         , chart_args: dict = {}
                         , titled_by: str = "name" # Name|
                         , chart_options: dict = DEFAULT_CHART_OPTIONS
                         ) -> tuple[Axes,list[Line2D]|BarContainer]:
        """
        :param chart_type: line, bar, column
        :param titled_by: name|number
        """        
        if not axes: axes = plt.gca() 
        data  = [chapt.stats.word_count for chapt in self.chapters]        
        labels = self.get_chapter_axis_labels(titled_by)
        chart = self.plot_chart_type(axes, data, labels, chart_type=chart_type, **chart_args)
        self.set_label_ticks(axes,labels,xaxes_options=xaxes_options,chart_type=chart_type)
        self.set_title(axes,title)
        if data_labels: self.data_labels(axes, chart, data, **data_label_options)        
        return axes,chart
    
    def set_axes(self, axes: Axes, **options):
        xaxis = options.get("xaxis", True)
        yaxis = options.get("yaxis", True)
        if not xaxis: axes.xaxis.set_label([])
        if not yaxis: axes.yaxis.set_label([])

    def badwords_by_chapter(self
                        , axes: Axes = None
                        , chart_type: str = "column"
                        , title: str = "Filthy Words by Chapter"
                        , data_labels: bool = False
                        , data_label_options: dict = {"fmt": ",","offset": 0, "rotation": 0, "font_dict": {'weight' : 'bold','size': 10}}
                        , xaxes_options: dict = { "rotation": 45 }
                        , chart_args: dict = {}
                        , titled_by: str = "name" # Name|
                        , ignore_empty: bool = False
                        ) -> tuple[Axes,list[Line2D]|BarContainer]:
        """
        :param chart_type: line, bar, column
        :param titled_by: name|number
        """        
        if not axes: axes = plt.gca() 
        filtered_chapters = [chapt for chapt in self.chapters if chapt.stats.badword_count or 0 > 0] if ignore_empty else self.chapters
        if chart_type == "bar":
            filtered_chapters.reverse()
        data  = [chapt.stats.badword_count for chapt in filtered_chapters]
        labels = self.get_chapter_axis_labels(titled_by, filtered_chapters)
        chart = self.plot_chart_type(axes, data, labels, chart_type=chart_type, **chart_args)
        self.set_label_ticks(axes,labels,xaxes_options=xaxes_options,chart_type=chart_type)
        self.set_title(axes,title)
        if data_labels:
            if chart_type in ["bar","column"]:
                self.data_labels_bars(axes, chart, data, **data_label_options)        
        
        return axes,chart

    def top_badwords(self
                         , axes: Axes = None
                         , chart_type: str = "column"
                         , title: str = "Filth in Book"
                         , data_labels: bool = False
                         , data_label_options: dict = {"fmt": ",","offset": 0, "rotation": 0, "font_dict": {'weight' : 'bold','size': 10}}
                         , xaxes_options: dict = { "rotation": 45 }
                         , chart_args: dict = {}
                         , top_n: int = 10
                         ) -> tuple[Axes,list[Line2D]|BarContainer]:
        """
        :param chart_type: line, bar, column
        :param titled_by: name|number
        """        
        if not axes: axes = plt.gca()
        bad_words = {}
        for chapter in self.chapters:
            for word,val in chapter.bad_words.items():                
                bad_words[word] = bad_words.get(word, 0) + val        
        if len(bad_words.keys()) < 1: 
            print("No bad words found, good job being a pure and unblemished pillar of morality!")
            return
        bad_words = dict(sorted(bad_words.items(), key=lambda item: item[1], reverse=True))
        data,labels = list(bad_words.values())[:top_n],list(bad_words.keys())[:top_n]
        # labels = self.get_chapter_axis_labels(titled_by)
        chart = self.plot_chart_type(axes, data, labels, chart_type=chart_type, **chart_args)
        self.set_label_ticks(axes,labels,xaxes_options=xaxes_options,chart_type=chart_type)
        self.set_title(axes,title)
        if data_labels:            
            if chart_type in ["bar","column"]:
                self.data_labels_bars(axes, chart, data, **data_label_options)
        return axes,chart 
    
    def top_words(self
                         , axes: Axes = None
                         , chart_type: str = "column"
                         , title: str = "Top Words"
                         , data_labels: bool = False
                         , data_label_options: dict = {"fmt": ",","offset": 0, "rotation": 0, "font_dict": {'weight' : 'bold','size': 10}}
                         , xaxes_options: dict = { "rotation": 45 }
                         , chart_args: dict = {}
                         , top_n: int = 10
                         ) -> tuple[Axes,list[Line2D]|BarContainer]:
        """
        :param chart_type: line, bar, column
        :param titled_by: name|number
        """        
        if not axes: axes = plt.gca()
        words = {}
        for chapter in self.chapters:
            for word,val in chapter.words.items():                
                words[word] = words.get(word, 0) + val        
        if len(words.keys()) < 1: 
            print("No bad words found, good job being a pure and unblemished pillar of morality!")
            return
        words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
        data,labels = list(words.values())[:top_n],list(words.keys())[:top_n]
        # labels = self.get_chapter_axis_labels(titled_by)
        chart = self.plot_chart_type(axes, data, labels, chart_type=chart_type, **chart_args)        
        self.set_label_ticks(axes,labels,xaxes_options=xaxes_options,chart_type=chart_type)
        self.set_title(axes,title)
        if data_labels:
            if chart_type in ["bar","column"]:
                self.data_labels_bars(axes, chart, data, **data_label_options)
        return axes,chart 
        
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

    def data_labels_lines(self
                         , axes: Axes
                         , lines: list[Line2D]
                         , labels: list[str]
                         , fmt=","
                         , offset: int = None
                         , rotation=0
                         , font_dict={'weight' : 'normal','size': 10}):
        offset = offset or 0.5
        i=0
        while i < len(labels):
            label = f"{labels[i]: {fmt}}"  
            axes.text(i, labels[i] + offset, f'{label}',
                    ha='center', va='bottom', fontdict=font_dict,rotation=rotation)
            i += 1

    def words(self
            , axes: Axes = None
            ) -> tuple[Axes,list[Line2D]|BarContainer]:
        """
        :param chart_type: line, bar, column
        :param titled_by: name|number
        """        
        if not axes: axes = plt.gca()
        words = {}
        for chapter in self.chapters:
            for word,val in chapter.words.items():                
                words[word] = words.get(word, 0) + val        
        if len(words.keys()) < 1: 
            print("No bad words found, good job being a pure and unblemished pillar of morality!")
            return
        
        wc = WordCloud().generate_from_frequencies(words)        
        axes.imshow(wc)
        axes.set_axis_off()
        return axes,wc
    
    def bad_words(self
            , axes: Axes = None
            ) -> tuple[Axes,list[Line2D]|BarContainer]:
        """
        :param chart_type: line, bar, column
        :param titled_by: name|number
        """        
        if not axes: axes = plt.gca()
        words = {}
        for chapter in self.chapters:
            for word,val in chapter.bad_words.items():                
                words[word] = words.get(word, 0) + val        
        if len(words.keys()) < 1: 
            print("No bad words found, good job being a pure and unblemished pillar of morality!")
            return
        
        wc = WordCloud().generate_from_frequencies(words)        
        axes.imshow(wc)
        axes.set_axis_off()
        return axes,wc

    def set_title(self, axes: Axes, title: str):
        axes.set_title(title)
    
    def set_label_ticks(self, axes: Axes, labels, xaxes_options, chart_type):
        if chart_type == "bar":
            axes.set_yticks(axes.get_yticks())
            axes.set_yticklabels(labels,**xaxes_options)
        else:
            axes.set_xticks(axes.get_xticks())
            axes.set_xticklabels(labels,**xaxes_options)

    def get_chapter_axis_labels(self, titled_by: str="name", filter_chapters: list[Chapter]|None = None):
        titled_by = titled_by.lower()
        chapters = filter_chapters if filter_chapters else self.chapters
        if titled_by == "name":
            return [chapt.name for chapt in chapters]
        else:
            return [f"Chapter {chapt.number}" for chapt in chapters]
    
    def data_labels(self
                    , axes: Axes
                    , chart: BarContainer|list[Line2D]
                    , labels: list[str]
                    , fmt=","
                    , offset=None
                    , rotation=0
                    , font_dict={'weight' : 'normal','size': 10}):
        if isinstance(chart,BarContainer): self.data_labels_bars(axes,chart,labels,fmt,offset,rotation,font_dict)
        if isinstance(chart,list): self.data_labels_lines(axes,chart,labels,fmt,offset,rotation,font_dict)

    def plot_chart_type(self, axes: Axes, data: list[float|int], labels: list[str|datetime|int], chart_type: str = "column", **chart_args) -> list[Line2D]|BarContainer:
        if chart_type == "line":
            return axes.plot(labels,data,**chart_args)
        if chart_type == "column":
            return axes.bar(labels,data,**chart_args)
        if chart_type == "bar":
            return axes.barh(labels,data,**chart_args)