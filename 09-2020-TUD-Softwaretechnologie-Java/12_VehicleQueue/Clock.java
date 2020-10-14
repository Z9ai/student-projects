import java.util.ArrayList;
import java.util.List;

public class Clock {
    private int currentTime  = 0;
    private int endOfTime;
    private List<ClockObserver> observers = new ArrayList();

    public Clock(int endOfTime) {
        if (endOfTime<currentTime){
            throw new IllegalArgumentException();
        }
        this.endOfTime = endOfTime;
    }

    public void addObserver(ClockObserver observer){
        observers.add(observer);
    }

    public void removeObserver(ClockObserver observer){
        observers.remove(observer);
    }

    public int getCurrentTime() {
        return currentTime;
    }

    public void run(){
        currentTime = 0;
        while (currentTime < endOfTime){
            currentTime = currentTime +1;
            this.tick(currentTime);
        }
    }

    private void tick(int currentTime){
        for (ClockObserver observer :  observers){
            observer.tick(currentTime);
        }
    }
}
