from bookstats import *
from bookstats import *
from bookstats import *

if __name__ == "__main__":
    import filedialpy, matplotlib, os
    from matplotlib import pyplot as plt
    path = filedialpy.openFile()
    fig, axes = plt.subplots(2,2, squeeze=False)
    matplotlib.use('qtagg')
    

    (_,wordCountPlot),(_,wordCloud),(_,filthPlot),(_,topWordsPlot) = enumerate(axes.flat)
    book = Book(path)
    _,__ = book.reports.words_by_chapter(axes=wordCountPlot,titled_by="number",chart_type="line")
    _,__ = book.reports.words(axes=wordCloud)
    _,__ = book.reports.top_words(axes=topWordsPlot, xaxes_options={"rotation": 90})
    _,__ = book.reports.badwords_by_chapter(axes=filthPlot,chart_type="bar",xaxes_options={"rotation": 0})

    plt.tight_layout(pad=2)

    # https://stackoverflow.com/questions/26084231/draw-a-separator-or-lines-between-subplots

    # Draw a horizontal lines at those coordinates
    line = plt.Line2D([0,1],[0.51,0.51], transform=fig.transFigure, color="black")
    fig.add_artist(line)
    line = plt.Line2D([0.546,0.546],[1,0], transform=fig.transFigure, color="black")
    fig.add_artist(line)
    plt.show()
    