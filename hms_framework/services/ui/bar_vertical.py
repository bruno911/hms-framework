import base64
from hms_framework.interfaces.ui.chart import Chart
import pandas as pd
import matplotlib.pyplot as plt
import io


class BarVertical(Chart):

    def base64_image(self):
        df = pd.DataFrame({'date': self.dates, 'count': self.counts})

        ax = df.plot.bar(x='date', y='count')

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