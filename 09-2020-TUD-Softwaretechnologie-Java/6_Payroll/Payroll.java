import java.util.List;

public class Payroll{
    private PayrollDisposition disposition;
    private int payday;

    public Payroll(PayrollDisposition disposition, int payday){
        if(payday <1  || payday > 30){
            throw new IllegalArgumentException();
        }
        if(disposition == null){
            throw new NullPointerException();
        }
        this.disposition = disposition;
        this.payday = payday;
    }

    public void doPayroll(PayrollDB db) {
        if(db == null){
            throw new NullPointerException();
        }
        List<Employee> employees = db.getEmployeeList();
        for(Employee employee : employees){
            try {
                if(employee.isPayday(payday)) {
                    disposition.sendPayment(employee, employee.calculatePay());
                }
            }
            catch(UnpayableEmployeeException exception){}
        }
    }
}
