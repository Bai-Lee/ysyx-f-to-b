from evidence import *
import zipfile,shutil

def audit_run(r):
    folder=ROOT/'artifacts'/r['name'];assert r['status']=='PASS' and r['inputs_unchanged']
    assert json.loads((folder/'run.json').read_text('utf8'))==r
    for name in ('stdout','stderr'):assert sha(folder/(name+'.log'))==r[name+'_sha256']
    with zipfile.ZipFile(folder/'input_snapshot.zip') as z:
        for i,f in enumerate(r['inputs']):
            assert sha(f['path'])==f['sha256']
            assert hashlib.sha256(z.read(f'{i:02d}_{Path(f["path"]).name}')).hexdigest()==f['sha256']

def main():
    p=ROOT/'reports/E2_results.json';data=json.loads(p.read_text('utf8'));assert data['status']=='PASS_ALTERNATIVE'
    assert sha(data['source'])==data['source_sha256'] and sha(data['compiler']['path'])==data['compiler']['sha256']
    for r in data['native_runs']:audit_run(r)
    assert len(data['controls'])==3
    for r in data['controls']:
        assert r['status']=='PASS';audit_run(r['compile']);audit_run(r['execute'])
        assert r['execute']['exit_code']==1 and 'AssertionError' in (ROOT/'artifacts'/r['execute']['name']/'stderr.log').read_text('utf8')
    assert {r['name'] for r in data['online']}=={'normal','asan_ubsan'}
    for r in data['online']:
        assert r['status']=='PASS' and r['didExecute'] and r['exit_code']==0
        assert sha(r['request'])==r['request_sha256'] and sha(r['response'])==r['response_sha256']
        request=json.loads(Path(r['request']).read_text('utf8'));assert request['source']==Path(data['source']).read_text('utf8')
    now=datetime.now(timezone.utc).isoformat()
    audit={'status':'PASS','timestamp':now,'node':'E2','route':'official independent linked-list competence branch','main_task':'E2-M001','native_selftest_operations_per_optimization':20000,'optimization_levels':['O0','O2'],'python_oracle_operations':12525,'compiled_faults_rejected':3,'online_execution':['normal','asan_ubsan'],'source_sha256':data['source_sha256'],'all_CEX_exercises_completed':False,'scope_limits':['Official E2 permits the independent linked-list competence branch; individual textbook exercises were not done and are not marked PASS.','Native host is Windows x86-64; Compiler Explorer sanitizer execution is remote Linux, not an installed local Linux environment.','Finite tests and sanitizer success are not an unlimited proof of all possible memory behavior.'],'evidence':'reports/E2_results.json'}
    dump(ROOT/'reports/E2_AUDIT.json',audit)
    ledger=ROOT/'config/task_status.json';backup=ROOT/'config/history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');backup.mkdir(parents=True);shutil.copyfile(ledger,backup/'task_status.json')
    state=json.loads(ledger.read_text('utf8'))
    for row in state['tasks']:
        if row['id']=='E2-M001':row.update(status='PASS',implementation_status='PASS',completion_route='OFFICIAL_COMPETENCE_BRANCH',evidence=[str(ROOT/'E/E2/linked_list.c'),str(ROOT/'reports/E2_AUDIT.json'),str(ROOT/'reports/E2_REPORT.md')],result_details='Independently implemented and debugged a C linked list, recursion/pointers, allocation-failure rollback; native, Python oracle and Compiler Explorer sanitizer validation passed. Officially permitted exemption branch; no claim of all textbook exercises.',updated=now)
        elif row['id'].startswith('CEX-'):row.update(applicability='EXEMPT_UNDER_SELECTED_E2_COMPETENCE_BRANCH',branch_reason='E2 public lecture explicitly permits independent linked-list competence alternative. Individual exercise status remains truthful; these were not executed.')
    state.update(current_stage='E2',stage_status='PASS',next_stage='E3',stop_after_F=False);dump(ledger,state)
    report=f'''# E2 C语言程序设计验收报告

E2-M001：PASS，采用v26.07原文允许的“能独立编写链表并调试正确后跳过章节学习”分支。没有声称完成全部CEX逐章练习；这些条目的NOT_RUN保留，并注明当前分支豁免。更新时间：{now}。

独立交付：[linked_list.c](../E/E2/linked_list.c)。实现按位置插入、读取、删除、反转、清空、快照和稳定归并排序，维护head/tail/length不变量；递归拆分排序展示递归，链节点及指针更新展示动态内存和指针。分配失败发生在连接修改之前，因此插入失败保持原链表不变。

| 实际运行 | 结果 |
|---|---|
| 本机MSYS2 GCC15.2，C17严格警告当错误 | O0/O2均编译及执行通过，各20,000次操作 |
| Python通过DLL调用真实C API | 12,525次操作，与两个独立Python列表逐步比较 |
| 边界与内存管理 | 空表、单元素、头中尾、重复值、INT_MIN/MAX、越界及SIZE_MAX、分配失败、部分/零容量快照通过 |
| 故障对照 | 反转丢尾指针、排序方向错误、分配失败破坏长度，3/3编译成功后被独立断言拒绝 |
| Compiler Explorer gcc15.1 | 真实编译执行20,000次操作，退出0 |
| Compiler Explorer ASan+UBSan | 真实带检测编译执行，退出0，无ASan/UBSan诊断；活跃节点计数0 |
| 最终审计 | 输入快照、源码、工具、命令结果和网络请求/响应哈希一致 |

算法：插入/读取/删除按位置遍历O(n)，头部操作O(1)；反转O(n)且原地改边；归并排序先用快慢指针分半，递归深度O(log n)，两条有序链迭代合并，时间O(n log n)。比较用关系运算，避免用相减比较INT_MIN/MAX时溢出。归并相等值先取左侧节点，因此稳定。

参考模型采用连续数组/Python列表，未复用链表指针算法。每步检查无环、长度、尾节点、完整值序列与活跃节点计数，部分快照还检查缓冲区哨兵。测试覆盖有限；本机计数器不等同于通用内存检查器，所以另运行了线上ASan/UBSan。线上Linux成功不等于本机E3的Linux环境已安装。

曾遇到O2对空参考数组的maybe-uninitialized警告，已显式初始化参考数组并保留失败日志，没有关闭-Werror或删除断言。

重放：[Run-E2.ps1](../scripts/Run-E2.ps1)。默认离线重跑本机测试并核验相同源码的既有线上证据；加-Online再次运行Compiler Explorer并审计。源码变化后不能复用旧线上结果。在线请求仅含本项目自行编写的链表源代码。原始网络响应保存在artifacts/E2/compiler_explorer。[机器结果](E2_results.json)和[审计](E2_AUDIT.json)可逐项复核。

E2-O001扩展阅读不冒称全部完成。下一项E3需要真实本机Linux环境和Linux作业；当前尚未执行。
'''
    (ROOT/'reports/E2_REPORT.md').write_text(report,encoding='utf8');print('E2_FINAL_AUDIT PASS official competence branch',flush=True)

if __name__=='__main__':main()
