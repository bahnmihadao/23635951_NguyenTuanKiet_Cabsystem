"""Validate YAML, OpenAPI 3.0, references and README requirement coverage."""
import re
from pathlib import Path
import yaml
from openapi_spec_validator import validate

root=Path(__file__).resolve().parent
spec=yaml.safe_load((root/'openapi.yaml').read_text(encoding='utf-8'))
validate(spec)
ops=[(p,m,o) for p,methods in spec['paths'].items() for m,o in methods.items()]
ids=[o['operationId'] for _,_,o in ops]
assert len(ids)==len(set(ids)), 'Duplicate operationId'
def walk(v):
    if isinstance(v,dict):
        if '$ref' in v:
            target=spec
            assert v['$ref'].startswith('#/'),v['$ref']
            for part in v['$ref'][2:].split('/'):target=target[part]
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
walk(spec)
readme=(root.parent/'README.md').read_text(encoding='utf-8')
fr=set(re.findall(r'FR\d{2}\.\d+',readme))
uc=set(re.findall(r'UC\d{3}',readme))
covered_fr={f for _,_,o in ops for f in o['x-readme-fr']}
covered_uc={u for _,_,o in ops for u in o['x-readme-use-cases']}
assert not fr-covered_fr, f'Missing FR: {fr-covered_fr}'
assert not uc-covered_uc, f'Missing UC: {uc-covered_uc}'
assert not covered_fr-fr, f'Unknown FR: {covered_fr-fr}'
assert not covered_uc-uc, f'Unknown UC: {covered_uc-uc}'
for path,method,o in ops:
    path_params={p['name'] for p in o.get('parameters',[]) if p.get('in')=='path'}
    assert path_params==set(re.findall(r'\{([^}]+)\}',path)),path
    assert o['description'] and o['responses']
print(f'PASS OpenAPI {spec["openapi"]}: {len(ops)} operations; {len(spec["components"]["schemas"])} schemas; all local references valid; {len(fr)}/{len(fr)} FR and {len(uc)}/{len(uc)} UC covered.')
lines=['# CAB System API – hướng dẫn sử dụng','','- File chính: `openapi.yaml` (OpenAPI 3.0.3).','- Đây là hợp đồng API đề xuất từ README, chưa phải backend đã triển khai.','- Mở https://editor.swagger.io/ và import file YAML để đọc tài liệu.','- Khi có backend, sửa `servers.url`, đăng nhập lấy token rồi dùng Authorize để gọi thử.','- Các mục chưa chốt, giới hạn đồ án và quy tắc dùng chung nằm trong `info.description`.','- `x-readme-fr`, `x-readme-use-cases` và `x-readme-business-rules` dùng đối chiếu yêu cầu.','- `build_openapi.py` là nguồn sinh file; sửa nguồn rồi chạy lại nếu muốn duy trì tự động. PyYAML là tùy chọn khi sinh, giúp định dạng dễ đọc.','- `validate_openapi.py` cần PyYAML và openapi-spec-validator; kiểm tra chuẩn, tham chiếu, operationId, path parameters và độ phủ mã yêu cầu.','',f'Đã kiểm tra: {len(ops)} thao tác trên {len(spec["paths"])} đường dẫn; {len(fr)} FR và {len(uc)} UC có trong README. Bao phủ UC001–UC016; tác vụ tự động như điều phối và phát thông báo được mô tả ở các API kích hoạt và truy vấn liên quan.','','## Ma trận yêu cầu → API','','| Yêu cầu | API |','|---|---|']
for f in sorted(fr|uc):
    mapped=[f'`{m.upper()} {p}`' for p,m,o in ops if f in o['x-readme-fr'] or f in o['x-readme-use-cases']]
    lines.append('| '+f+' | '+'<br>'.join(mapped)+' |')
(root/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

