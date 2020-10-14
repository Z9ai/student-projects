import java.time.LocalDate;
import java.util.*;

public class Adapter implements IProject{
    private Project project;

    public Adapter(String name, String description, double rate){
        project = new Project(name, description, rate);
    }

    public void setTask(Task newTask){
        project.setTask(newTask);
    }

    public double getDuration(){
        return project.getDuration();
    }

    public long getTotalCost(){
        return project.getTotalCost();
    }

    public List<Deliverable> getDeliverables(){
        List<Deliverable> tempList = new ArrayList();
        Map<LocalDate, List<Deliverable>> tempMap = project.allDeliverables();
        for(Map.Entry entry: tempMap.entrySet()){
            tempList.addAll((ArrayList)(entry.getValue()));
        }
        return tempList;
    }
}