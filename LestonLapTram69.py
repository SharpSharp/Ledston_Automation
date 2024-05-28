import jarray
import jmri

tram69Running = 1

class LoopTram69(jmri.jmrit.automat.AbstractAutomaton) :
        
    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print "Inside init(self)LoopTram69"
        # set up sensor numbers
        # fwdSensor is reached when loco is running forward
        self.terminusNearSensor = sensors.provideSensor("CS2")
        self.crossoverRearSensor = sensors.provideSensor("CS3")
        self.crossoverNearSensor = sensors.provideSensor("CS4")
        self.terraceRearSensor = sensors.provideSensor("CS5")
        self.terraceNearSensor = sensors.provideSensor("CS6")
        self.terminusThrownSensor = sensors.provideSensor("CS7")
        self.terminusClosedSensor = sensors.provideSensor("CS8")
        
        self.bankRearSensor = sensors.provideSensor("CS2001")
        self.bankNearSensor = sensors.provideSensor("CS2002")
        self.odeonNearSensor = sensors.provideSensor("CS2003")
        self.odeonRearSensor = sensors.provideSensor("CS2004")
        self.pubRearSensor = sensors.provideSensor("CS2005")
        self.pubNearSensor = sensors.provideSensor("CS2006")
        self.pubThrownSensor = sensors.provideSensor("CS2007")
        self.pubClosedSensor = sensors.provideSensor("CS2008")
        
        self.bandstandRearSensor = sensors.provideSensor("CS3001")
        self.bandstandNearSensor = sensors.provideSensor("CS3002")
        
        self.fairgoundMainSensor = sensors.provideSensor("CS4002")
        self.fairgoundReverserSensor = sensors.provideSensor("CS4003")
        self.fairgoundExitSensor = sensors.provideSensor("CS4004")
        self.fairThrownSensor = sensors.provideSensor("CS4007")
        self.fairClosedSensor = sensors.provideSensor("CS4008")
        
        self.schoolRearSensor = sensors.provideSensor("CS5001")
        self.schoolNearSensor = sensors.provideSensor("CS5002")
        
        self.keepRunning = memories.getMemory("IM69")
        
        print "assign tram 69"
        # get loco address. For long address change "False" to "True"
        self.tram = self.getThrottle(69, False)
        # tram running speed between 0.00 amd 1.00 different for each tram
        self.speed = 0.6  
        # Set tram Forward
        self.tram.setIsForward(True)
        
    def startTram(self):
        print "Start Tram 69"
        self.acceleratingSpeed = 0
        while self.acceleratingSpeed < self.speed:
            self.tram.setSpeedSetting(self.acceleratingSpeed)
            self.waitMsec(10)
            self.acceleratingSpeed = self.acceleratingSpeed + 0.02     
            
        self.tram.setSpeedSetting(self.speed)
        
    def stopTram(self):
        print "Stop Tram 69"
        self.speed  = self.tram.getSpeedSetting()
        self.decceleratingSpeed = self.speed
        while self.decceleratingSpeed > 0:
            self.tram.setSpeedSetting(self.decceleratingSpeed)
            self.waitMsec(10)
            self.decceleratingSpeed = self.decceleratingSpeed - 0.02
            
        self.tram.setSpeedSetting(0)
        
    def routeFromTerminusNear(self):
        self.waitSensorInactive(self.crossoverNearSensor)
        self.waitSensorInactive(self.crossoverRearSensor)
        print "crossover clear for 69"
        self.waitSensorInactive(self.terraceRearSensor)
        print "Terrace clear for 69"
        
    def routeToBandstandRear(self):
        self.waitSensorInactive(self.bandstandRearSensor)
        print "Bandstand clear for 69"
    
    def routeToPubRear(self):
        self.waitSensorInactive(self.bankRearSensor)
        print "Bank clear for 69, check turnout"
        turnouts.provideTurnout("CT2001").setState(CLOSED)
        self.waitSensorActive(self.pubClosedSensor)
        print "Turnout closed"
        self.waitSensorInactive(self.odeonRearSensor)
        print "Oden clear for 69"
        self.waitSensorInactive(self.pubRearSensor)
        print "Pub clear for 69"
        
    def routeToFair(self):
        print "check fiar turnout"
        turnouts.provideTurnout("CT4001").setState(THROWN)
        self.waitSensorActive(self.fairThrownSensor)
        print "Wait for fair Sensor"
        self.waitSensorInactive(self.fairgoundMainSensor)
        self.waitSensorInactive(self.fairgoundReverserSensor)
        
    def routeFromFair(self):
        self.waitSensorInactive(self.fairgoundReverserSensor)
        self.waitSensorInactive(self.fairgoundExitSensor)
    def routeToPubNear(self):
        self.waitSensorInactive(self.pubNearSensor)
    def routeFromPubNear(self):
        turnouts.provideTurnout("CT2001").setState(CLOSED)
        self.waitSensorActive(self.pubClosedSensor)
        print "Pub turnout Closed"
        self.waitSensorInactive(self.odeonNearSensor)
        print "Odeon near is clear for 69"
        self.waitSensorInactive(self.bankNearSensor)
        print "Bank near is clear for 69"
        
    def routeToBandstandNear(self):
        self.waitSensorInactive(self.bandstandNearSensor)
        print "Bandstand near is clear for 69"
        self.waitSensorInactive(self.terraceNearSensor)
        print "terrace near is clear for 69"
        
    def routeToTerminusNear(self):
        self.waitSensorInactive(self.crossoverNearSensor)
        print "crossover near is clear for 69"
        self.waitSensorInactive(self.terminusNearSensor)
        print "terminus near is clear for 69"
        self.waitSensorInactive(self.crossoverNearSensor)
        print "route clear for 69 set turnout"
        turnouts.provideTurnout("CT1").setState(CLOSED)
        print "Turnout told to closed wait for sensor"
        self.waitSensorActive(self.terminusClosedSensor)
        
    def handle(self):
        # handle() is called repeatedly until it returns false.
        print "Inside handle(self) LoopTram69"
        #wait 1 second for layout to catch up, then set speed
        print "69 wait to leave terminus"
        self.waitMsec(2000)
        self.routeFromTerminusNear()
        self.routeToBandstandRear()
        self.startTram()
        print "69 running to bandstand rear"
        
        self.waitSensorActive(self.bandstandRearSensor)
        self.waitMsec(800)
        print "69 arrived at bandstand rear"
        self.stopTram()
        
        print "69 wait to leave bandstand"
        self.waitMsec(4000)
        self.routeToPubRear()
        self.startTram()
        print "69 running to pub rear"
        
        self.waitSensorActive(self.pubRearSensor)
        print "69 arrive at pub rear"
        self.stopTram()
        
        print "69 wait to leave pub"
        self.waitMsec(4000)
        self.routeToFair()
        self.startTram()
        print "69 running to fair"
        
        self.waitSensorActive(self.fairgoundMainSensor)
        self.waitMsec(6200)
        print "69 arrived at fair"
        self.stopTram()
        
        print "69 wait to leave fair"
        self.routeFromFair()
        self.routeToPubNear()
        self.waitMsec(4000)
        self.startTram()
        print "69 running to pub near"
        
        self.waitSensorActive(self.pubNearSensor)
        self.waitMsec(500)
        print "69 arrived at pub near"
        self.stopTram()
        
        print "69 wait to leave pub near"
        self.waitMsec(4000)
        self.routeFromPubNear()
        self.routeToBandstandNear()
        self.startTram()
        print "69 running to bandstand near"
        
        self.waitSensorActive(self.terraceNearSensor)
        print "69 arrived at bandstand near"
        self.stopTram()
        
        print "69 wait to leave bandstand near"
        self.waitMsec(4000)
        self.routeToTerminusNear()
        self.startTram()
        print "69 running to terminus"
        
        self.waitSensorActive(self.terminusNearSensor)
        print "69 arrived at terminus"
        self.stopTram()
        
        print "toggle direction of 69"
        self.tram.setIsForward(False) if self.tram.isForward else self.tram.setIsForward(True)
        self.waitMsec(2000)
        turnouts.provideTurnout("CT1").setState(THROWN)
        self.waitSensorActive(self.terminusThrownSensor)
        print "Turnout thrown ready for"

        if tram69Running == 0:
            print "69 has Terminted"
            return 0

        return 1
        
        print "End of Loop"
# end of class definition
# start one of these up
LoopTram69().start()