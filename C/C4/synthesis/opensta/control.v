module control(input clock,output q);wire d,qn;INVX1H7L inv(.A(q),.Y(d));DFFX1H7L ff(.CK(clock),.D(d),.Q(q),.QN(qn));endmodule
