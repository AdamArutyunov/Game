from .Utils import LinearGradient, hex_to_rgb


class Effect:
    def __init__(self, start, duration):
        self.start = start
        self.duration = duration
        self.end = self.start + self.duration

    def affect(self, time):
        return {}


class BackgroundColorEffect(Effect):
    def __init__(self, start, duration):
        self.colorpoints = []

    def update(self, time, color):
        time = float(time)
        color = hex_to_rgb(color)

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


EFFECTS = {
    'effect': Effect,
    'background_color': BackgroundColorEffect,
}
