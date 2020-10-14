import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

public class Team extends AbstractEnterpriseUnit{
    StaffMember teamLeader;
    List<StaffMember> teamMembers = new ArrayList<>();

    public Team(String name, StaffMember teamLeader){
        super(name);
        this.teamLeader = teamLeader;
    }

    public StaffMember getTeamLeader(){
        return teamLeader;
    }

    public List<StaffMember> getTeamMembers(){
        return teamMembers;
    }
}
