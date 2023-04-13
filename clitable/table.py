class Table:
    def __init__(self, headers, data=None):
        self.headers = headers
        self.data = data or []

    def add_row(self, row):
        if len(row) != len(self.headers):
            raise ValueError("Row length must match header length")
        self.data.append(row)

    def __iter__(self):
        # Skips the headers and iterates over the data only
        for row in self.data:
            yield row

    def get_headers(self):
        return self.headers
        
    def __str__(self):
        result = []
        result.append("|".join(self.headers))
        for row in self.data:
            result.append("|".join(str(value) for value in row))
        return "\n".join(result)



