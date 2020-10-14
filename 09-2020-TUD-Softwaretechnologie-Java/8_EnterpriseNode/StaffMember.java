import java.util.TreeSet;
import java.util.Set;

public class StaffMember  implements Comparable<StaffMember>{
    private String name;
    private String job;
    private Set<StaffMember> directSubordinates = new TreeSet<>();

    public StaffMember(String name, String job){
        this.name = name;
        this.job = job;
    }

    public String getJob(){
        return job;
    }

    public Set<StaffMember> getDirectSubordinates(){
        return directSubordinates;
    }

    public String getName(){
        return name;
    }

    public String toString(){
        return name;
    }

    public int compareTo(StaffMember m) {
        return name.compareTo(m.name);    // aufgrund toString könnte man auch "return this.compareTo(m);" schreiben
    }

    public boolean equals(Object m){
        return name.equals(((StaffMember)m).getName());
    }

    public boolean addDirectSubordinate(StaffMember subordinate){
        return directSubordinates.add(subordinate);
    }

    public boolean removeDirectSubordinate(StaffMember subordinate){
        return directSubordinates.remove(subordinate);
    }



}
