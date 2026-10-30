"""Reproducible width/rank edits of the locked generated SoC; preserve its source."""
import re


def render(text,width,ranks):
    assert width in [16,32] and ranks in [1,2] and (width==32 or ranks==1)
    if width==16:return text
    substitutions={
        'sdram_bundle_cs':f'output [{ranks-1}:0]',
        'sdram_bundle_ras':'output',
        'sdram_bundle_dqm':f'output [{width//8-1}:0]',
        'sdram_bundle_dq':f'inout [{width-1}:0]',
        'sdram_cs':f'output [{ranks-1}:0]',
        'sdram_ras':'output',
        'sdram_dqm':f'output [{width//8-1}:0]',
        'sdram_dq':f'inout [{width-1}:0]',
        '_asic_sdram_cs':f'wire [{ranks-1}:0]',
        '_asic_sdram_dqm':f'wire [{width//8-1}:0]',
        '_dq_wire':f'wire [{width-1}:0]',
    }
    for name,kind in substitutions.items():
        pattern=r'(?m)^\s*(?:(?:output|inout|wire)\s*(?:\[\d+:\d+\])?\s*)?'+re.escape(name)+r'(?=[,;\t])'
        text,count=re.subn(pattern,'  '+kind+' '+name,text)
        assert count==1,(name,count)
    return text
