import re


class Transform():
    result = {}
    def __init__(self, extracted):
        self.extracted = extracted

    def transformLocations(self):
        result = {}
        for key, value in self.extracted.items():
            if key == 'location':
                cutted_value = re.search(': (.*),', value).group(1)
                result[key] = cutted_value
        return result
    def run(self):
        self.transformLocations()

if __name__ == '__main__':
    transf = Transform()
    transf.run()
