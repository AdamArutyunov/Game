from .Utils import LinearGradient


class Effect:
    slug = 'effect'

    def __init__(self, state, start, duration):
        self.start = start
        self.duration = duration
        self.end = self.start + self.duration

        self.state = state

    def affect(self, time):
        pass


class BackgroundColorEffect(Effect):
    slug = 'background_color'

    def __init__(self, start, duration):
        self.colorpoints = []

    def add_colorpoint(self, time, color):
        self.colorpoints.append((time, color))
        self.colorpoints.sort(key=lambda x: x[0])

    def affect(self, time):
        data = {}

        for i in range(len(self.colorpoints) - 1):
            time1, color1 = self.colorpoints[i]
            time2, color2 = self.colorpoints[i + 1]

            if time1 <= time < time2:
                color = LinearGradient.calculate(
                    color1,
                    color2,
                    (time - time1) / (time2 - time1)
                )

                data['background'] = color
                break

        return data
