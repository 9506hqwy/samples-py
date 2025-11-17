class Error0 { };
class Error1 { };
class Error2 { };
class Error3 { };

class NativeException {
    public:

    void exception0() throw(Error0);
    void exception1();
    void exception2() throw(Error2);;
    void exception3();
};
