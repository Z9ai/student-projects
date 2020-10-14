public class Appointee extends Employee{
    private int payday;
    private int hoursPerMonth;
    private double payPerHour;

    public Appointee(String id, int payday, int hoursPerMonth, double payPerHour) {
        super(id);
        if(payday<1||payday>30||hoursPerMonth<1||payPerHour<Double.MIN_VALUE){
            throw new IllegalArgumentException();
        }

        this.payday = payday;
        this.hoursPerMonth = hoursPerMonth;
        this.payPerHour = payPerHour;
    }

    @Override
    public boolean isPayday(int dayOfMonth) {
        if(dayOfMonth <1  || dayOfMonth > 30){
            throw new IllegalArgumentException();
        }
        if(this.payday == dayOfMonth){
            return true;
        }
        return false;
    }
    @Override
    public double calculatePay() {
        return   hoursPerMonth * payPerHour;
    }
    @Override
    public double calculateDeductions(){
        return 0.4 * hoursPerMonth * payPerHour;
    }
}
