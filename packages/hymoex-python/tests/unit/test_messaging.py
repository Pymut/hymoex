"""Tests for HIP message schemas."""

import pytest
from pydantic import ValidationError

from hymoex import (
    MsgPacket,
    ContextEnvelope,
    DecisionRequest,
    ExpertPayload,
    ExecCommand,
    ExecReceipt,
    Telemetry,
)


class TestMsgPacket:
    def test_valid(self):
        pkt = MsgPacket(channel="web", customer_id="c1", payload="hello")
        assert pkt.channel == "web"

    def test_invalid_channel(self):
        with pytest.raises(ValidationError):
            MsgPacket(channel="sms", customer_id="c1", payload="hello")

    def test_roundtrip(self):
        pkt = MsgPacket(channel="whatsapp", customer_id="c1", payload="test")
        restored = MsgPacket.model_validate_json(pkt.model_dump_json())
        assert restored.channel == pkt.channel


class TestExpertPayload:
    def test_confidence_bounds(self):
        ExpertPayload(confidence=0.0)
        ExpertPayload(confidence=1.0)

    def test_confidence_out_of_range(self):
        with pytest.raises(ValidationError):
            ExpertPayload(confidence=1.5)

        with pytest.raises(ValidationError):
            ExpertPayload(confidence=-0.1)


class TestTelemetry:
    def test_sentiment_bounds(self):
        Telemetry(sentiment=-1.0)
        Telemetry(sentiment=1.0)

    def test_sentiment_out_of_range(self):
        with pytest.raises(ValidationError):
            Telemetry(sentiment=2.0)


class TestExecCommand:
    def test_valid_types(self):
        for t in ["crm_update", "doc_generate", "payment", "calendar"]:
            cmd = ExecCommand(type=t)
            assert cmd.type == t

    def test_invalid_type(self):
        with pytest.raises(ValidationError):
            ExecCommand(type="invalid")


class TestContextEnvelope:
    def test_wraps_packet(self):
        pkt = MsgPacket(channel="voice", customer_id="c2", payload="help")
        env = ContextEnvelope(msg_packet=pkt, lead_stage="qualification")
        assert env.msg_packet.channel == "voice"
