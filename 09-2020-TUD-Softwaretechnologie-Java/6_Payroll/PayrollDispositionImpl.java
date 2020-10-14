import java.util.HashMap;
import java.util.Map;

public class PayrollDispositionImpl implements PayrollDisposition{
    private Map<Employee, Double> payments = new HashMap<>();

    public PayrollDispositionImpl(){
    }

    @Override
    public void sendPayment(Employee empl, double payment) {
        if(payment <= 0){
            throw new IllegalArgumentException();
        }
        if(empl == null){
            throw new NullPointerException();
        }
        try {
            double salary = empl.calculatePay() - empl.calculateDeductions();
            payments.put(empl,salary);
        }
        catch(UnpayableEmployeeException exception){}
    }

    public double getTotal(){
        double total = 0;
        for(Map.Entry payment : payments.entrySet()){
            total = total + (double) payment.getValue();
        }
        return total;
    }

    public double getAverage(){
        if(payments.size() == 0){
            return 0;
        }
        double total = this.getTotal();
        double average = total / payments.size();
        return average;
    }

    public Map<Employee, Double> getPayments() {
        return payments;
    }
}
