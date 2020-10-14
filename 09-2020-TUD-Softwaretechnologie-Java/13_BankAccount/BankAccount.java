public class BankAccount {
    private double balance = 0.0;
    private double lineOfCredit;
    private String accountNumber;
    private AccountState state;

    public BankAccount(String accountNumber, double lineOfCredit){
        if (accountNumber.equals("")){
            throw new IllegalArgumentException();
        }
        if (accountNumber == null){
            throw new NullPointerException();
        }
        this.accountNumber = accountNumber;
        this.lineOfCredit = lineOfCredit;
        state = new Positive();
    }

    public boolean payIn(double amount){
        if (amount <= 0){
            throw new IllegalArgumentException();
        }
        return state.payIn(amount);
    }

    public boolean payOff(double amount){
        if (amount <= 0){
            throw new IllegalArgumentException();
        }
        return state.payOff(amount);
    }

    public boolean close(){
        if (balance == 0.0){
            state = new Closed();
            return true;
        }
        return false;
    }

    public double getBalance(){
        return balance;
    }

    public String getState(){
        return state.toString();
    }

    public String getAccountNumber(){
        return accountNumber;
    }

    public void printBalance(){
        state.printBalance();
    }

    public void payInterest(){
        state.payInterest();
    }






    public abstract class AccountState {

        public boolean payIn(double amount){
            return false;
        }

        public boolean payOff(double amount){
            return false;
        }

        public String toString(){
            return state.toString();
        }

        public void payInterest(){
            throw new IllegalStateException();
        }

        public abstract void printBalance();
    }




    public class Positive extends AccountState {

        public String toString(){
            return "Positive";
        }

        public boolean payIn(double amount){
            balance = balance + amount;
            return true;
        }

        public boolean payOff(double amount){
            if (balance - amount >= 0){
                balance = balance - amount;
                return true;
            }
            else if (balance - amount == -lineOfCredit){
                balance = -lineOfCredit;
                state = new Frozen();
                return true;
            }
            else if (balance - amount < -lineOfCredit){
                return false;
            }
            else {
                balance = balance - amount;
                state = new Negative();
                return true;
            }
        }

        public void payInterest(){
            balance = balance * 1.01;
        }

        @Override
        public void printBalance() {
            System.out.println("Balance is POSITIVE: +"+ balance + ".");
        }
    }




    public class Negative extends AccountState {

        public boolean payIn(double amount){
            if (balance + amount >= 0){
                balance = balance + amount;
                state = new Positive();
                return true;
            }
            else {
                balance = balance + amount;
                return true;
            }
        }

        public boolean payOff(double amount){
            if (balance - amount == -lineOfCredit){
                balance = -lineOfCredit;
                state = new Frozen();
                return true;
            }
            else if (balance - amount < -lineOfCredit){

                return false;
            }
            else {
                balance = balance - amount;
                return true;
            }
        }

        public void payInterest(){
            balance = balance * 1.03;
            if(balance <= -lineOfCredit){
                state = new Frozen();
            }
        }

        public String toString(){
            return "Negative";
        }

        @Override
        public void printBalance() {
            System.out.println("Balance is NEGATIVE: "+ balance + ".");
        }
    }





    public class Frozen extends AccountState {

        public boolean payIn(double amount){
            if (balance + amount >= 0){
                balance = balance + amount;
                state = new Positive();
                return true;
            }
            balance = balance + amount;
            state = new Negative();
            return true;
        }

        public void payInterest(){
            balance = balance * 1.05;
        }

        public String toString(){
            return "Frozen";
        }

        @Override
        public void printBalance() {
            System.out.println("Balance is NEGATIVE: "+ balance + ". You need to pay in money.");
        }
    }





    public class Closed extends AccountState {

        public String toString(){
            return "Closed";
        }

        @Override
        public void printBalance() {
            System.out.println("This account is CLOSED. The balance is 0.");
        }
    }
}
