class cursor:
    x = 0
    y = 0

    def update_cursor(self, width, height):
        self.x = max(0, self.x)
        self.x = min(width-1, self.x)
        self.y = max(0, self.y)
        self.y = min(height-1, self.y)

