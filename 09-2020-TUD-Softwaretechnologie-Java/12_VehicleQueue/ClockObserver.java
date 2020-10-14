import java.time.Clock;
import java.util.ArrayList;
import java.util.List;

public interface ClockObserver {

    public void tick (int currentTime);
}
