module light(input clock,reset,output reg[15:0]led);
reg[31:0] count;
always @(posedge clock)begin
 if(reset)begin led<=16'd1;count<=0;end
 else begin if(count==0)led<={led[14:0],led[15]};count<=(count==32'd5000000)?32'd0:count+32'd1;end
end endmodule
