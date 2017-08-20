module type MT = sig
  (** Doc for Single *)
  exception Simple
  (** Doc' for Single *)

  (** Doc for Hidden *)
  exception Hidden [@@autodoc.hide]
  (** Doc' for Hidden *)

  (** Doc for SinglePayload *)
  exception SinglePayload of int
  (** Doc' for SinglePayload *)

  (** Doc for SeveralPayload *)
  exception SeveralPayload of int * float * string
  (** Doc' for SeveralPayload *)

  (** Doc for TuplePayload *)
  exception TuplePayload of (int * float * string)
  (** Doc' for TuplePayload *)

  (** Doc for RecordPayload *)
  exception RecordPayload of {
    a: int; (** Doc for RecordPayload.a *)
    mutable b: float; (** Doc for RecordPayload.b *)
  }
  (** Doc' for RecordPayload *)
end

include MT

(** A reference to an exception: :exn:`tests/Exceptions.Simple`. *)
