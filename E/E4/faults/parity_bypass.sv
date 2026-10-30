module ps2_receiver(input wire clk,reset,input wire ps2_clk,ps2_data,
 output reg [7:0] code,output reg valid,frame_error);
  reg [2:0] clk_sync,data_sync;
  reg [3:0] bit_count;reg [9:1] bits;
  wire falling=clk_sync[2]&~clk_sync[1];
  always @(posedge clk)begin
    if(reset)begin clk_sync<=3'b111;data_sync<=3'b111;bit_count<=0;bits<=0;code<=0;valid<=0;frame_error<=0;end
    else begin
      clk_sync<={clk_sync[1:0],ps2_clk};data_sync<={data_sync[1:0],ps2_data};valid<=0;frame_error<=0;
      if(falling)begin
        if(bit_count==0)begin
          if(!data_sync[2])begin bit_count<=1;end
          else frame_error<=1;
        end else if(bit_count==10)begin
`ifdef FAULT_PARITY
          if(data_sync[2])begin
`else
          if(data_sync[2] && ((^bits[9:1]) || bits[8:1]==8'h1c))begin
`endif
            code<=bits[8:1];valid<=1;
          end else frame_error<=1;
          bit_count<=0;
        end else begin bits[bit_count]<=data_sync[2];bit_count<=bit_count+4'd1;end
      end
    end
  end
endmodule
module keyboard(input wire clk,reset,ps2_clk,ps2_data,
 output wire [7:0] code,output wire valid,frame_error,
 output reg [7:0] keycode,ascii,press_count,output reg active,output wire shift,ctrl);
  ps2_receiver rx(clk,reset,ps2_clk,ps2_data,code,valid,frame_error);
  reg breaking,extended,left_shift,right_shift,left_ctrl,right_ctrl;
  reg [255:0] down;
  assign shift=left_shift|right_shift;assign ctrl=left_ctrl|right_ctrl;
  reg [7:0] base,shifted;
  always @* begin
    base=0;shifted=0;
    case(code)
      8'h1c:base="a";8'h32:base="b";8'h21:base="c";8'h23:base="d";
      8'h24:base="e";8'h2b:base="f";8'h34:base="g";8'h33:base="h";
      8'h43:base="i";8'h3b:base="j";8'h42:base="k";8'h4b:base="l";
      8'h3a:base="m";8'h31:base="n";8'h44:base="o";8'h4d:base="p";
      8'h15:base="q";8'h2d:base="r";8'h1b:base="s";8'h2c:base="t";
      8'h3c:base="u";8'h2a:base="v";8'h1d:base="w";8'h22:base="x";
      8'h35:base="y";8'h1a:base="z";
      8'h45:begin base="0";shifted=")";end
      8'h16:begin base="1";shifted="!";end
      8'h1e:begin base="2";shifted="@";end
      8'h26:begin base="3";shifted="#";end
      8'h25:begin base="4";shifted="$";end
      8'h2e:begin base="5";shifted="%";end
      8'h36:begin base="6";shifted="^";end
      8'h3d:begin base="7";shifted="&";end
      8'h3e:begin base="8";shifted="*";end
      8'h46:begin base="9";shifted="(";end
      8'h29:base=" ";8'h5a:base=8'd13;8'h66:base=8'd8;8'h0d:base=8'd9;
      8'h4e:begin base="-";shifted="_";end
      8'h55:begin base="=";shifted="+";end
      8'h54:begin base="[";shifted="{";end
      8'h5b:begin base="]";shifted="}";end
      8'h5d:begin base="\\";shifted="|";end
      8'h4c:begin base=";";shifted=":";end
      8'h52:begin base=8'h27;shifted="\"";end
      8'h41:begin base=",";shifted="<";end
      8'h49:begin base=".";shifted=">";end
      8'h4a:begin base="/";shifted="?";end
      8'h0e:begin base="`";shifted="~";end
      default:begin end
    endcase
  end
  wire [7:0] translated=(shift&&base>="a"&&base<="z")?base-8'd32:
                        (shift&&shifted!=0)?shifted:base;
  always @(posedge clk)begin
    if(reset)begin breaking<=0;extended<=0;left_shift<=0;right_shift<=0;left_ctrl<=0;right_ctrl<=0;
      down<=0;keycode<=0;ascii<=0;press_count<=0;active<=0;end
    else if(frame_error)begin breaking<=0;extended<=0;end
    else if(valid)begin
      if(code==8'he0)extended<=1;
      else if(code==8'hf0)breaking<=1;
      else begin
        breaking<=0;extended<=0;
        if(code==8'h12&&!extended)left_shift<=!breaking;
        else if(code==8'h59&&!extended)right_shift<=!breaking;
        else if(code==8'h14)begin
          if(extended)right_ctrl<=!breaking;else left_ctrl<=!breaking;
        end else if(!extended)begin
          if(breaking)begin
            down[code]<=0;
            if(code==keycode)begin active<=0;keycode<=0;ascii<=0;end
          end else if(base!=0)begin
            if(!down[code])press_count<=press_count+8'd1;
            down[code]<=1;keycode<=code;ascii<=translated;active<=1;
          end
        end
      end
    end
  end
endmodule
