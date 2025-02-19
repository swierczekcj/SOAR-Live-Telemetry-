double x = 0;
int graph_base = 0;
String old_state;
double graph;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
    String state = Serial.readString();
    if(state == "LAUNCH"){
      old_state = "LAUNCH";
    } else if (state == "STOP"){
      old_state = "STOP";
    }
  }
  if (old_state == "LAUNCH"){
      graph = sin(x);
      Serial.print("Base:");
      Serial.print(graph_base);
      Serial.print(",");
      Serial.print("Random Garbage:");
      Serial.println(graph);
      x = x + .05;
      old_state = "LAUNCH";
    } else if (old_state == "STOP"){
      graph = 0;
      // Serial.print("Base:");
      // Serial.print(graph_base);
      // Serial.print(",");
      // Serial.print("Random Garbage:");
      // Serial.println(graph);
      old_state = "STOP";
    }
}

