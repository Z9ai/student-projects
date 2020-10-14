import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class VehicleQueue implements ClockObserver {
    private double entryDelay;
    private double exitDelay;
    private int trafficLightRate;
    private boolean greenLight = false;
    private VehicleGenerator generator;
    private List<Vehicle> queue = new ArrayList<>();
    private double greenCounter = 0;

    public VehicleQueue(double entryDelay, double exitDelay, int trafficLightRate, VehicleGenerator generator) {
        if(trafficLightRate<=0 || entryDelay <=0 || exitDelay <=0){
            throw new IllegalArgumentException();
        }
        if(generator == null){
            throw new NullPointerException();
        }
        this.entryDelay = entryDelay;
        this.exitDelay = exitDelay;
        this.trafficLightRate = trafficLightRate;
        this.greenLight = greenLight;
        this.generator = generator;
    }
    
    public void enter(){
        queue.add(generator.createVehicle());
    }

    public void leave(){
        if(queue.size() != 0){
            queue.remove(0);
        }
    }

    @Override
    public void tick(int currentTime) {
        int iterationTime = (currentTime-1)%trafficLightRate;
        System.out.println(iterationTime);
        if (iterationTime == 0){
            if ((currentTime/trafficLightRate)%2 == 1){
                greenLight = true;
                greenCounter = Math.round(10 * (currentTime - 1 + exitDelay))/10.0;
            }
            else{
                greenLight = false;
            }
        }
        double timeTemp = 0;
        while(timeTemp<=currentTime){
            if (timeTemp > currentTime-1) {
                    this.enter();
                    System.out.println("car entered.");
            }
            timeTemp = Math.round(10*(timeTemp + entryDelay))/10.0;
            System.out.println(timeTemp);
        }
        if(greenLight == true) {
            System.out.println("greenLight: "+greenLight);
            while (greenCounter <= currentTime) {
                this.leave();
                greenCounter = Math.round(10*(greenCounter + exitDelay))/10.0;
                System.out.println("car leaves.");
            }
        }
    }

    public double getLength(){
        double size = 0;
        for(Vehicle vehicle: queue){
            size = size + vehicle.getLength();
        }
        return size;
    }

    public int getSize(){
        return queue.size();
    }
}
