DEFAULT_JSON = {
  "meta": {
    "comments": ""
  },
  "layout": {
    "partner_spacing": 1.5,
    "min_sib_spacing": 1.0,
    "gen_height": 3.0,
    "family_gap": 1.0,
    "u_shape_offset": 3.0,
    "adjustment_iterations": 1,
    "layout_priority": "Children to Parents (Top-down)",
    "symbol_size": 1.0,
    "line_width": 1.5,
    "font_size": 10,
    "label_offset": 0.2,
    "node_width": 1
  },
  "individual": [
    {
      "id": "I-1",
      "gender": "M",
      "affected": "",
      "label": "paternal\ngrandfather",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "I-2",
      "gender": "F",
      "affected": "",
      "label": "paternal\ngrandmother",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "I-3",
      "gender": "M",
      "affected": "",
      "label": "maternal\ngrandfather",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "I-4",
      "gender": "F",
      "affected": "",
      "label": "maternal\ngrandmother",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-1",
      "gender": "M",
      "affected": "",
      "label": "father",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-2",
      "gender": "F",
      "affected": "",
      "label": "mother",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-1",
      "gender": "M",
      "affected": "A",
      "label": "self",
      "proband": True,
      "client": True,
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-2",
      "gender": "F",
      "affected": "",
      "label": "wife",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-1",
      "gender": "F",
      "affected": "",
      "label": "daughter",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    }
  ],
  "relationships": [
    {
      "p1": "I-1",
      "p2": "I-2",
      "divorced": "",
      "children": [
        "II-1"
      ],
      "multiples": [],
      "adopted_in": [],
      "adopted_out": [],
      "consanguinity": ""
    },
    {
      "p1": "I-3",
      "p2": "I-4",
      "divorced": "",
      "children": [
        "II-2"
      ],
      "multiples": [],
      "adopted_in": [],
      "adopted_out": [],
      "consanguinity": ""
    },
    {
      "p1": "II-1",
      "p2": "II-2",
      "divorced": "",
      "children": [
        "III-1"
      ],
      "multiples": [],
      "adopted_in": [],
      "adopted_out": [],
      "consanguinity": ""
    },
    {
      "p1": "III-1",
      "p2": "III-2",
      "divorced": "",
      "children": [
        "IV-1"
      ],
      "multiples": [],
      "adopted_in": [],
      "adopted_out": [],
      "consanguinity": ""
    }
  ]
}


REFERENCE_JSON = {
  "meta": {
    "comments": "$\\mathbf{INPUT\\ METHODS}$  \n$\\mathbf{BoldText}$: \\$\\mathbf{BoldText}\\$  \n$\\mathit{ItalicText}$: \\$\\mathit{ItalicText}\\$  \n$\\mathbf{Line break}$: '\\n' or 'Shift+Enter'  \n\n$X^{sup}$: \\$X_{sub}\\$  \n$X_{sub}$: \\$X^{sup}\\$  \n$\\alpha, \\beta, \\gamma$: \\$\\alpha, \\beta, \\gamma\\$  \n\n$\\mathbf{Germline}$: $\\mathit{BRCA1}$: c.188T>A, p.L63X  \n$\\mathbf{Created\\ by}$: John Smith| Date: 2026-01-01  \nFree comments"
  },
  "layout": {
    "partner_spacing": 3.0,
    "min_sib_spacing": 2.0,
    "gen_height": 8.0,
    "family_gap": 0.0,
    "u_shape_offset": 0.5,
    "adjustment_iterations": 1,
    "layout_priority": "Children to Parents (Top-down)",
    "symbol_size": 2.0,
    "line_width": 1.5,
    "font_size": 8,
    "label_offset": 0.5,
    "node_width": 1
  },
  "individual": [
    {
      "id": "I-1",
      "gender": "M",
      "affected": "",
      "label": "divorced: D_p1",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "I-2",
      "gender": "F",
      "affected": "",
      "label": "deceased: True",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": True,
      "pregnancy": ""
    },
    {
      "id": "I-3",
      "gender": "M",
      "affected": "",
      "label": "consanguinity: True",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "I-4",
      "gender": "F",
      "affected": "",
      "label": "divorced: D_p2",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-1",
      "gender": "M",
      "affected": "A2-1",
      "label": "affected: \nA2-1",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-2",
      "gender": "M",
      "affected": "D",
      "label": "affected: D",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-3",
      "gender": "F",
      "affected": "A2-2",
      "label": "affected: \nA2-2",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-4",
      "gender": "M",
      "affected": "A4-1",
      "label": "affected: \nA4-1",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-5",
      "gender": "F",
      "affected": "A2-1,A4-3,A4-4",
      "label": "affected: \nA2-1,A4-3,A4-4",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-6",
      "gender": "F",
      "affected": "",
      "label": "II-2+II-3:\nmonozygotic",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-7",
      "gender": "F",
      "affected": "",
      "label": "",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-8",
      "gender": "F",
      "affected": "",
      "label": "II-4+II-5:\ndizygotic",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-9",
      "gender": "F",
      "affected": "",
      "label": "",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-10",
      "gender": "F",
      "affected": "",
      "label": "II-6+II-7:\nunknown",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "II-11",
      "gender": "F",
      "affected": "D",
      "label": "affected: D",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-1",
      "gender": "F",
      "affected": "",
      "label": "AMAB: \nAssigned \nMale \nat Birth",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-2",
      "gender": "M",
      "affected": "A",
      "label": "proband: True\nclient: True\naffected: A",
      "proband": True,
      "client": True,
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-3",
      "gender": "F",
      "affected": "",
      "label": "documented: \nTrue",
      "proband": "",
      "client": "",
      "documented": True,
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-4",
      "gender": "F",
      "affected": "C",
      "label": "affected: C",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-5",
      "gender": "N",
      "affected": "",
      "label": "pregnancy: \nTrue",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": True
    },
    {
      "id": "III-6",
      "gender": "M",
      "affected": "",
      "label": "adopted_in: \nIII-6",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-7",
      "gender": "F",
      "affected": "",
      "label": "adopted_out:\nIII-7",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "III-8",
      "gender": "M",
      "affected": "",
      "label": "AFAB: \nAssigned \nFemale \nat Birth",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-1",
      "gender": "M",
      "affected": "",
      "label": "gender: M",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-2",
      "gender": "F",
      "affected": "",
      "label": "gender: F",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-3",
      "gender": "N",
      "affected": "",
      "label": "gender: N\n(Non-binary)",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-4",
      "gender": "A",
      "affected": "",
      "label": "gender: A\n(Abortion)\n(Spontaneous)",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-5",
      "gender": "A",
      "affected": "",
      "label": "gender: A \ndeceased: True\n(Termination)",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": True,
      "pregnancy": ""
    },
    {
      "id": "IV-6",
      "gender": "I",
      "affected": "",
      "label": "gender: I \n(Infertility)",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-7",
      "gender": "NC",
      "affected": "",
      "label": "gender: NC\n(No Children)",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-8",
      "gender": "M2",
      "affected": "",
      "label": "gender: M2",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-9",
      "gender": "F3",
      "affected": "",
      "label": "gender: F3",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    },
    {
      "id": "IV-10",
      "gender": "Nn",
      "affected": "",
      "label": "gender: Nn",
      "proband": "",
      "client": "",
      "documented": "",
      "deceased": "",
      "pregnancy": ""
    }
  ],
  "relationships": [
    {
      "p1": "I-1",
      "p2": "I-2",
      "divorced": "D_p1",
      "children": [
        "II-1",
        "II-3",
        "II-4"
      ],
      "adopted_in": [],
      "adopted_out": [],
      "multiples": [],
      "consanguinity": ""
    },
    {
      "p1": "I-3",
      "p2": "I-4",
      "divorced": "D_p2",
      "children": [
        "II-5",
        "II-6",
        "II-7",
        "II-8",
        "II-9",
        "II-10",
        "II-11"
      ],
      "adopted_in": [],
      "adopted_out": [],
      "multiples": [
        {
          "ids": [
            "II-6",
            "II-7"
          ],
          "type": "monozygotic"
        },
        {
          "ids": [
            "II-8",
            "II-9"
          ],
          "type": "dizygotic"
        },
        {
          "ids": [
            "II-10",
            "II-11"
          ],
          "type": "unknown"
        }
      ],
      "consanguinity": True
    },
    {
      "p1": "II-2",
      "p2": "",
      "divorced": "",
      "children": [
        "III-1"
      ],
      "adopted_in": [],
      "adopted_out": [],
      "multiples": [],
      "consanguinity": ""
    },
    {
      "p1": "II-3",
      "p2": "",
      "divorced": "",
      "children": [
        "III-1"
      ],
      "adopted_in": [],
      "adopted_out": [],
      "multiples": [],
      "consanguinity": ""
    },
    {
      "p1": "II-4",
      "p2": "II-5",
      "divorced": "",
      "children": [
        "III-2",
        "III-4",
        "III-5",
        "III-6",
        "III-7",
        "III-8"
      ],
      "adopted_in": [
        "III-6"
      ],
      "adopted_out": [
        "III-7"
      ],
      "multiples": [],
      "consanguinity": ""
    },
    {
      "p1": "III-2",
      "p2": "III-3",
      "divorced": "",
      "children": [
        "IV-1",
        "IV-2",
        "IV-3",
        "IV-4",
        "IV-5",
        "IV-6",
        "IV-7",
        "IV-8",
        "IV-9",
        "IV-10"
      ],
      "adopted_in": [],
      "adopted_out": [],
      "multiples": [],
      "consanguinity": ""
    },
    {
      "p1": "II-11",
      "p2": "",
      "divorced": "",
      "children": [
        "III-8"
      ],
      "adopted_in": [],
      "adopted_out": [],
      "multiples": [],
      "consanguinity": ""
    }
  ]
}