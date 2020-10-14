public class Volunteer extends Employee {

    public Volunteer (String id) {
        super(id);
    }

    @Override
    public boolean isPayday(int dayOfMonth) {
        if(dayOfMonth <1  || dayOfMonth > 30){
            throw new IllegalArgumentException();
        }
        return false;
    }

    @Override
    public double calculatePay() throws UnpayableEmployeeException {
        throw new UnpayableEmployeeException("Not an Apointee.");
    }

    @Override
    public double calculateDeductions() {
        return 0;
    }
}
