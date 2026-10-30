/* Blocking parameterized instruction cache; refill metadata commits atomically. */
module ysyx_00000000_icache #(
  parameter integer LINES=16,WORDS=1,WAYS=1,
  parameter bit USE_BURST=0,FAULT_TAG=0
)(
  input wire clock,reset,invalidate,
  input wire q_valid,input wire [31:0] q_addr,output wire q_ready,
  output wire p_valid,output wire [31:0] p_data,output wire [1:0] p_error,input wire p_ready,
  output wire m_valid,output wire [31:0] m_addr,output wire [7:0] m_len,input wire m_ready,
  input wire r_valid,input wire [31:0] r_data,input wire [1:0] r_error,input wire r_last,output wire r_ready,
  output wire event_access,event_hit,event_miss,event_bypass,event_fill
);
  localparam integer SETS=LINES/WAYS,WORD_BITS=$clog2(WORDS),SET_BITS=$clog2(SETS);
  localparam integer TAG_BITS=32-2-WORD_BITS-SET_BITS;
  localparam integer INDEX_WIDTH=$clog2(LINES)>0?$clog2(LINES):1;
  localparam [2:0] IDLE=0,REQUEST=1,FILL=2,RESPONSE=3;
  reg [2:0] state;
  reg [LINES-1:0] valid;
  reg [TAG_BITS-1:0] tags[0:LINES-1];
  reg [31:0] data[0:LINES*WORDS-1];
  reg [SETS-1:0] replace_way;
  reg [31:0] address,response_data;
  reg [1:0] response_error,fill_error;
  reg [INDEX_WIDTH-1:0] selected_line;
  reg [3:0] beat;
  reg cached,burst,poison;
  wire [31:0] query_set=(q_addr>>(2+WORD_BITS))&32'(SETS-1);
  wire [31:0] query_word=(q_addr>>2)&32'(WORDS-1);
  wire [TAG_BITS-1:0] query_tag=TAG_BITS'(q_addr>>(2+WORD_BITS+SET_BITS));
  wire query_cacheable=(q_addr>=32'h30000000&&q_addr<32'h31000000)||
    (q_addr>=32'h80000000&&q_addr<32'h80400000)||(q_addr>=32'ha0000000&&q_addr<32'ha8000000);
  reg hit;reg [INDEX_WIDTH-1:0] hit_line,victim_line;
  integer w;
  always @*begin
    hit=0;hit_line=0;victim_line=INDEX_WIDTH'(query_set*WAYS+(WAYS==2?32'(replace_way[query_set]):0));
    for(w=0;w<WAYS;w=w+1)begin
      if(valid[query_set*WAYS+w]&&(FAULT_TAG||tags[query_set*WAYS+w]==query_tag))begin
        hit=1;hit_line=INDEX_WIDTH'(query_set*WAYS+w);
      end
      if(!valid[query_set*WAYS+w])victim_line=INDEX_WIDTH'(query_set*WAYS+w);
    end
  end
  assign q_ready=!reset&&state==IDLE&&!invalidate;
  assign p_valid=!reset&&state==RESPONSE;
  assign p_data=response_data;assign p_error=response_error;
  assign m_valid=!reset&&state==REQUEST;
  assign m_addr=cached?((address&~32'(WORDS*4-1))+(burst?0:{26'b0,beat,2'b0})):address;
  assign m_len=burst?8'(WORDS-1):8'b0;
  assign r_ready=!reset&&state==FILL;
  assign event_access=q_valid&&q_ready;
  assign event_hit=event_access&&query_cacheable&&hit;
  assign event_miss=event_access&&query_cacheable&&!hit;
  assign event_bypass=event_access&&!query_cacheable;
  assign event_fill=r_valid&&r_ready&&cached&&(beat==WORDS-1)&&fill_error==0&&r_error==0;
  wire [31:0] held_word=(address>>2)&32'(WORDS-1);
  wire finish=!cached||(beat==WORDS-1)||(burst&&r_last);
  wire [1:0] current_error=fill_error|r_error|((r_last!=(burst?(beat==WORDS-1):1'b1))?2'b10:2'b00);
  always @(posedge clock)begin
    if(reset)begin
      state<=IDLE;valid<=0;replace_way<=0;address<=0;response_data<=0;response_error<=0;
      fill_error<=0;selected_line<=0;beat<=0;cached<=0;burst<=0;poison<=0;
    end else begin
      case(state)
        IDLE:if(event_access)begin
          address<=q_addr;response_error<=0;fill_error<=0;beat<=0;poison<=0;
          cached<=query_cacheable;burst<=USE_BURST&&WORDS>1&&q_addr>=32'ha0000000&&q_addr<32'ha8000000;
          if(query_cacheable&&hit)begin
            response_data<=data[32'(hit_line)*WORDS+query_word];state<=RESPONSE;
            if(WAYS==2)replace_way[query_set]<=!hit_line[0];
          end else begin
            selected_line<=victim_line;state<=REQUEST;
            if(query_cacheable)valid[victim_line]<=0;
          end
        end
        REQUEST:if(m_valid&&m_ready)state<=FILL;
        FILL:if(r_valid&&r_ready)begin
          fill_error<=current_error;
          if(cached)data[32'(selected_line)*WORDS+{28'b0,beat}]<=r_data;
          if(!cached||held_word=={28'b0,beat})response_data<=r_data;
          if(finish)begin
            response_error<=current_error;state<=RESPONSE;
            if(cached&&!poison&&!invalidate&&current_error==0)begin
              tags[selected_line]<=TAG_BITS'(address>>(2+WORD_BITS+SET_BITS));valid[selected_line]<=1;
              if(WAYS==2)replace_way[(address>>(2+WORD_BITS))&32'(SETS-1)]<=!selected_line[0];
            end
          end else begin beat<=beat+1;if(!burst)state<=REQUEST;end
        end
        RESPONSE:if(p_ready)state<=IDLE;
        default:state<=IDLE;
      endcase
      if(invalidate)begin valid<=0;if(state!=IDLE)poison<=1;end
    end
  end
`ifndef SYNTHESIS
  initial begin
    if(LINES<2||(LINES&(LINES-1))||WORDS<1||WORDS>8||(WORDS&(WORDS-1))||(WAYS!=1&&WAYS!=2)||LINES<WAYS)$fatal(1,"ICACHE_PARAMETERS");
  end
`endif
endmodule
