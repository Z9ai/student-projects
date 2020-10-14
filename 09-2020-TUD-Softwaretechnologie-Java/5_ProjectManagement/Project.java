import java.time.LocalDate;
import java.util.*;

public class Project {
    private String name;
    private String description;
    private Task mainTask;

    public Project(String name, String description, double rate){
        if(name == "" || description == "" ){
            throw new IllegalArgumentException();
        }
        if(name == null || description == null ){
            throw new NullPointerException();
        }
        if(rate <= 0){
            throw new IllegalArgumentException();
        }
        this.name = name;
        this.description = description;
        mainTask = new Task(name, description, rate);
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public void setTask(Task newTask){
        if(newTask == null){
            throw new NullPointerException();
        }
        mainTask = newTask;
    }

    public double getDuration(){
        return mainTask.getTimeRequired();
    }

    public long getTotalCost(){
        return mainTask.getCostEstimate();
    }

    public Map<LocalDate, List<Deliverable>> allDeliverables() {
        List<Deliverable> deliverables = mainTask.allDeliverables();
        Map<LocalDate,List<Deliverable>> mapDeliverables = new HashMap();
        for(Deliverable deliverable: deliverables){
            mapDeliverables.put(deliverable.getDate(), new ArrayList<Deliverable>());
        }
        for(Deliverable deliverable: deliverables){
            mapDeliverables.get(deliverable.getDate()).add(deliverable);
        }
        return mapDeliverables;
    }
}