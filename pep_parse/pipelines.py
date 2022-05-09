import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.pep_sum = {}
        self.total_sum = 0

    def process_item(self, item, spider):
        self.total_sum += 1
        status = item['status']
        self.pep_sum[status] = self.pep_sum.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        dir_path = BASE_DIR / 'results'
        dir_path.mkdir(exist_ok=True)
        now = dt.datetime.now()
        file_name = f'status_summary_{now.strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        file_path = dir_path / file_name
        with open(file_path, mode='w', encoding='utf-8') as f:
            results = ['Статус,Количество\n']
            for status, count in self.pep_sum.items():
                results.append(f'{status},{count}\n')
            results.append(f'Total,{self.total_sum}')
            f.writelines(results)
