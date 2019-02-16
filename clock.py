import machine
import utime

# Standard layout for a seven segment display -
#      aa
#     f  b
#      gg
#     e  c
#      dd

digitSegments = [
#    a  b  c  d  e  f  g
    [1, 1, 1, 1, 1, 1, 0], # Digit 0
    [0, 1, 1, 0, 0, 0, 0], # Digit 1
    [1, 1, 0, 1, 1, 0, 1], # Digit 2
    [1, 1, 1, 1, 0, 0, 1], # Digit 3
    [0, 1, 1, 0, 0, 1, 1], # Digit 4
    [1, 0, 1, 1, 0, 1, 1], # Digit 5
    [1, 0, 1, 1, 1, 1, 1], # Digit 6
    [1, 1, 1, 0, 0, 0, 0], # Digit 7
    [1, 1, 1, 1, 1, 1, 1], # Digit 8
    [1, 1, 1, 1, 0, 1, 1], # Digit 9
    [1, 1, 1, 0, 1, 1, 1], # Digit A
    [0, 0, 1, 1, 1, 1, 1], # Digit b
    [1, 0, 0, 1, 1, 1, 0], # Digit C
    [0, 1, 1, 1, 1, 0, 1], # Digit d
    [1, 0, 0, 1, 1, 1, 1], # Digit E
    [1, 0, 0, 0, 1, 1, 1], # Digit F
]

# Segment positions are based off Rob's diagram. "(unit * 3) + channel"
segmentPositions = [
#    aaaaaaa, bbbbbbb, ccccccc, ddddddd, eeeeeee, fffffff, gggggggg,
    [(6*3)+0, (6*3)+2, (7*3)+0, (7*3)+2, (2*3)+2, (6*3)+1, (8*3)+0], # Minutes (units)
    [(5*3)+0, (5*3)+2, (8*3)+2, (2*3)+1, (2*3)+0, (5*3)+1, (8*3)+1], # Minutes (tens)
    [(4*3)+0, (4*3)+1, (3*3)+2, (1*3)+0, (1*3)+2, (4*3)+2, (3*3)+1], # Hours (units)
]

tenHourPosition = (1*3)+1
separatorPosition = (3*3)+0

# Rob's diagram indexed RGB units from 1, we need from 0, so reduce all positions by 3
segmentPositions = [[position - 3 for position in digit] for digit in segmentPositions]
tenHourPosition = tenHourPosition - 3
separatorPosition = separatorPosition - 3

def scalePositionList(brightness, output):
    return [value * brightness for value in output]

def positionListToTupleList(positions):
    if (len(positions) % 3 != 0):
        raise ValueError("List length must be divisible by 3 to create (r,g,b) tuples")
    result = []
    for i in range(0, len(positions), 3):
        result.append((positions[i], positions[i+1], positions[i+2]))
    return result

def setSeparator(value, output):
    output[separatorPosition] = value

def setSegments(values, positions, output):
    if (len(values) != len(positions)):
        raise ValueError("Value and position arrays must have equal length")
    for i in range(len(positions)):
        output[positions[i]] = values[i]

def setDigit(value, digit, output):
    setSegments(digitSegments[value], segmentPositions[digit], output)

def setMinutes(minutes, output):
    if (minutes < 0 or minutes > 99):
        raise ValueError("Minutes must be between 0 and 99")
    units = minutes % 10
    tens = (minutes - units) // 10
    setDigit(units, 0, output)
    setDigit(tens, 1, output)

def setHours(hours, output):
    if (hours < 0 or hours > 19):
        raise ValueError("Hours must be between 0 and 19")
    units = hours % 10
    output[tenHourPosition] = 1 if hours > 9 else 0
    setDigit(units, 2, output)

def setTime(hours, minutes, output):
    setHours(hours, output)
    setMinutes(minutes, output)

def generateClock(hours, minutes, isSeparatorShown = True, brightness = 255):
    unscaledOutput = [0 for _ in range(8*3)] # 8 RGB Units (3 channels each)
    setTime(hours, minutes, unscaledOutput)
    if (isSeparatorShown):
        setSeparator(1, unscaledOutput)
    return positionListToTupleList(scalePositionList(brightness, unscaledOutput))

def clockSet(hours, minutes, seconds = 0):
    now = list(machine.RTC().datetime())
    now[4] = hours
    now[5] = minutes
    now[6] = seconds
    now[7] = 0
    machine.RTC().datetime(tuple(now))

def testClock():
    isSeparatorShow = True
    while True:
        _,_,_,_,h,m,s,ms = machine.RTC().datetime()
        if (h > 12):
            h = h - 12
        
        print('{:02}{}{:02} = '.format(h, ':' if isSeparatorShow else ' ',m), generateClock(h, m, isSeparatorShow))
        isSeparatorShow = not isSeparatorShow
        utime.sleep_ms(1000 - ms)

