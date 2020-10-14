import java.util.Set;
import java.util.TreeSet;

public class StaffMemberIterator implements EnterpriseNodeIterator{
    private Set<StaffMember> allMembers = new TreeSet<>();

    public StaffMemberIterator(Set<StaffMember> directSubordinates){
        for(StaffMember member: directSubordinates){
            findSubordinatesRecursively(member);
        }
    }

    private void findSubordinatesRecursively(StaffMember m) {
        allMembers.add(m);
        for (StaffMember member : m.getDirectSubordinates()) {
            findSubordinatesRecursively(member);
        }
    }

    public boolean hasNext() {
        return (!allMembers.isEmpty());
    }

    public EnterpriseNode next(){
        return ((EnterpriseNode)((TreeSet)allMembers).first());
    }



}
