import base64
import matplotlib.pyplot as plt
import io
import pandas as pd

from hms_framework.interfaces.ui.chart import Chart


class BarHorizontal(Chart):

    def base64_image(self):
        df = pd.DataFrame({'date': self.dates, 'count': self.counts})
        ax = df.plot.barh(x='date', y='count', rot=0)

        plt.xlabel('Date')
        plt.ylabel('Count')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()
        graphic_base64 = base64.b64encode(image_png)
        graphic_base64 = graphic_base64.decode('utf-8')

        return graphic_base64
