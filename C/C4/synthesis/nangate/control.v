module control(input clock,a,output y);wire q;DFF_X1 ff(.CK(clock),.D(a),.Q(q));INV_X1 inv(.A(q),.ZN(y));endmodule
