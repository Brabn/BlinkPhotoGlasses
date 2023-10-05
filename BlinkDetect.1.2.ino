
/* Blink detection
 *  v 1.2 dated 04.09.17
 */
 
#define BLINKSENSOR A4
#define BLINKCONTROL 10
#define BLINKDIOD 13
#define MinBlinkTime 10		// min sensor duration for blink detection, ms
#define MaxBlinkTime 400	// max sensor duration for blink detection, ms
#define MinBlinkPause 500	// min duration for next blink detection, ms
#define EyeOpenLevel 450 	// max sensor level for open eyes
#define EyeCloseLevel 450   // min sensor level for close eyes
#define MinDifference 15	// min sensor difference for blink detection
#define MinDiffNoice 2

#define EyeOpenForStart 3000 // min time of open eye detection for start check
#define EyeCloseForStop 5000 // min time of open eye detection for start check

#define Frequency 20	// sensor frequency, ms
int CurentBlinkSensor=0;
bool Detection =false;
bool EyeState=false;
bool PrevEyeState=false;
int LastMin=0;
int LastMax=1024;
int LastState=0;
int CurrState=0;
int CurrDiff=0;
int LastDiff=0;
unsigned long DetectEyeTimer;
unsigned long OpenEyeTimer;
unsigned long CloseEyeTimer;
#define AverageCount 3	
class Average
{
  public:
  int LastValues[AverageCount];
  int AverageValue;
  int AverageSum;

  int num;
  Average()
  {
   AverageValue=0;
   AverageSum=0;
   num=0;
  }
  void Clear()
  {
       for (int i=0; i<AverageCount; i++)
      {
         LastValues[i]=0;
         AverageValue=0;
   		 AverageSum=0;
  		 num=0;

      }
  }
  int GetAverage()
  {

     for (int i=0; i<AverageCount; i++)
      {
         AverageSum+=LastValues[i];
      }
    AverageValue=((double)AverageSum/(double)AverageCount);
    AverageSum=0;
     
    
    return AverageValue;
  }
  void AddValue(double newValue)
  {
    LastValues[num++]=newValue;
    
    if (num>=AverageCount) num=0;
  }
};


//int AllPotState[PotCount*ControllerCount];
Average BlinkState;


void setup() {
  // declare the ledPin as an OUTPUT:
  pinMode(BLINKCONTROL,OUTPUT);
  digitalWrite(BLINKCONTROL, LOW);
    pinMode(BLINKDIOD,OUTPUT);
  digitalWrite(BLINKDIOD, LOW);
  pinMode(BLINKSENSOR, INPUT);           // set pin to input
  Serial.begin(9600);
  Serial.println("Blink Detection v1.2");
  OpenEyeTimer=millis();
  CloseEyeTimer=millis();
}

void loop() {
	if (millis()>3000)
	if ((millis()-DetectEyeTimer)>Frequency)
	{
		
		CurrState=analogRead(BLINKSENSOR);	// Read sensor value	
		if (CurrState<LastMin) LastMin=CurrState;
		if (CurrState>LastMax) LastMax=CurrState;
		
		BlinkState.AddValue(CurrState-LastState);
		LastState=CurrState;
		
		LastDiff=CurrDiff;
		CurrDiff=BlinkState.GetAverage();
		if (((LastDiff-CurrDiff)>MinDiffNoice)&&(LastDiff>MinDifference))
		{
			if (!EyeState)
			{
				EyeState=true;
				OpenEyeTimer=millis();
				if (((OpenEyeTimer-CloseEyeTimer)<=MaxBlinkTime)&&((OpenEyeTimer-CloseEyeTimer)>=MinBlinkTime))
				{
					Serial.print("BLINK ! time ");
					Serial.print((OpenEyeTimer-CloseEyeTimer));
					Serial.print(", diff ");
					Serial.println(LastDiff);
					digitalWrite(BLINKCONTROL, HIGH);
					digitalWrite(BLINKDIOD, HIGH);
					delay(MinBlinkPause);
					digitalWrite(BLINKCONTROL, LOW);
					digitalWrite(BLINKDIOD, LOW);
				}
			}
	   /* Serial.print("Open Diff:");
		Serial.println(LastDiff);*/
		}
		if (((CurrDiff-LastDiff)>MinDiffNoice)&&(LastDiff<MinDifference))
		{
			if (EyeState)
			{
				EyeState=false;
				CloseEyeTimer=millis();
			}
	   /* Serial.print(" close Diff:");
		Serial.println(LastDiff);*/
			
		}
		/*if (CurrDiff>0)		// opening eye
		{
			OpenEyeTimer=millis();
			if (((OpenEyeTimer-CloseEyeTimer)<=MaxBlinkTime)&&((OpenEyeTimer-CloseEyeTimer)>=MinBlinkTime))
			{
				Serial.print("BLINK ! time ");
				Serial.print((OpenEyeTimer-CloseEyeTimer));
				Serial.print(", diff ");
				Serial.println(CurrDiff);
				digitalWrite(BLINKCONTROL, HIGH);
				delay(200);
				digitalWrite(BLINKCONTROL, LOW);
			}
			
			
		}
		if (CurrDiff<0)		// closing eye
		{
			CloseEyeTimer=millis();
		}
		*/
		
		/*
		PrevEyeState=EyeState;						// Save previous state
		DetectEyeTimer=millis();
		if (CurentBlinkSensor>EyeOpenLevel)
		{
			EyeState=true;
		}
		if (CurentBlinkSensor<EyeCloseLevel)
		{
			EyeState=false;
		}*/
		
/*
		if (!EyeState && PrevEyeState)				// eye closing detected
		{
			CloseEyeTimer=millis();
			//Serial.println("Close eye");
		}
		if (EyeState && !PrevEyeState)				// eye opening detected
		{
			if (((CloseEyeTimer-OpenEyeTimer)<=MaxBlinkTime)&&((CloseEyeTimer-OpenEyeTimer)>=MinBlinkTime))
			{
				Serial.print("BLINK ! ");
				Serial.print((CloseEyeTimer-OpenEyeTimer));
			}
			OpenEyeTimer=millis();
			//Serial.println("Open eye");
		}
		*/
		/*if (EyeState&&((millis()-OpenEyeTimer)>EyeOpenForStart)&&(!Detection))
		{
			Detection=true;
			Serial.println("Start detection");
		}
		if (!EyeState&&((millis()-CloseEyeTimer)>EyeCloseForStop)&&(Detection))
		{
			Detection=false;
			Serial.println("Stop detection");
		}
		*/
		DetectEyeTimer=millis();
	}
}
