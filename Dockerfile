FROM python:3.14-slim

# 1. สร้าง User nonroot
RUN adduser --uid 1234 nonroot

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY src /src
WORKDIR /src

# รัน collectstatic (ไฟล์ที่ได้จะเป็นของ root)
RUN python manage.py collectstatic

# -----------------------------------------------------------------
# 2. (จุดสำคัญที่ขาดไป) โอนกรรมสิทธิ์โฟลเดอร์ /src ให้ nonroot
# -----------------------------------------------------------------
# ถ้าไม่มีบรรทัดนี้ nonroot จะเขียน Database ไม่ได้ครับ
RUN chown -R nonroot:nonroot /src

# (Optional) โอน venv ด้วยเผื่อต้องลงอะไรเพิ่ม
RUN chown -R nonroot:nonroot /venv

ENV DJANGO_DEBUG_FALSE=1

# 3. สลับ User เป็น nonroot (ตอนนี้เขียนไฟล์ได้แล้ว)
USER nonroot

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind :7860 superlists.wsgi:application"]
