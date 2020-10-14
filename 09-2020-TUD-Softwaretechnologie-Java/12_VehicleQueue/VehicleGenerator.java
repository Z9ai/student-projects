import java.util.Random;

public class VehicleGenerator {
    private Random randomGenerator = new Random();

    public VehicleGenerator(){
    }

    public Vehicle createVehicle(){
        int x = randomGenerator.nextInt(3);
        if (x == 0){
            return new Bus();
        }
        if (x == 1){
            return new Car();
        }
        else{
            return new Bicycle();
        }
    }
}
