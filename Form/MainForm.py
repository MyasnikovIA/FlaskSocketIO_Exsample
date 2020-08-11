def Designer():
    return """object DesignForm: TRootForm
  object HTMLEditText1: TButton
    Left = 56
    Top = 64
    Width = 200
    Height = 26
    Text = 'HTMLEditText1'
    Visible = True
    TypeInput = Password
  end
  object HTMLDiv1: TPanel
    Left = 48
    Top = 112
    Width = 344
    Height = 190
    Text = 'HTMLDiv1'
    Visible = True
    object HTMLLabel1: TLabel
      Left = 32
      Top = 16
      Width = 90
      Height = 18
      Text = 'HTMLLabel1'
      Visible = True
    end
    object HTMLLabel2: TLabel
      Left = 32
      Top = 40
      Width = 90
      Height = 18
      Text = 'HTMLLabel2'
      Visible = True
    end
    object HTMLLabel3: TLabel
      Left = 32
      Top = 64
      Width = 90
      Height = 18
      Text = 'HTMLLabel3'
      Visible = True
    end
  end
end"""


def init(args):
    print(Designer())


def getForm(args):
    all_vars = globals().copy()
    for key in all_vars:
        if key == '__builtins__':
            # del all_vars[key]
            continue
        if type(all_vars[key]).__name__ == 'function':
            continue
        print(key, '->', type(all_vars[key]).__name__ )
        print(key, '->', all_vars[key])
    print('================')

    loc = locals().copy()
    for key in loc:
        if key == 'all_vars':
            continue
        print(key, '->', loc[key])