import java.util.ArrayList;
import java.util.List;

public class Task extends ProjectItem{
    private List<ProjectItem> projectItems = new ArrayList();

    public Task(String name, String details, double rate){
        super(name, details, rate);
    }

    @Override
    public double getTimeRequired(){
        double timeRequired = 0;
        for (ProjectItem projectitem : projectItems){
            timeRequired = timeRequired + projectitem.getTimeRequired() ;
        }
        return timeRequired;
    }

    @Override
    public long getMaterialCost(){
        long materialCost = 0;
        for (ProjectItem projectitem : projectItems){
            materialCost = materialCost + projectitem.getMaterialCost() ;
        }
        return materialCost;
    }

    public void addProjectItem(ProjectItem pi){
        if(pi == null){
            throw new NullPointerException();
        }
        projectItems.add(pi);
    }

    public void removeProjectItem(ProjectItem pi){
        if(pi == null){
            throw new NullPointerException();
        }
        projectItems.remove(pi);
    }

    public List<Deliverable> allDeliverables(){
        List<Deliverable> deliverables = new ArrayList();
        for (ProjectItem projectitem : projectItems){
            if (projectitem instanceof Task) {
                deliverables.addAll(((Task) projectitem).allDeliverables());
            }
            else{
                deliverables.add((Deliverable) projectitem);
            }
        }
        return deliverables;
    }
}