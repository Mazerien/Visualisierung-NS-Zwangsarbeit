<?php
 return [
  'name' => 'housing',
  'label' => 'Unterkunft',
  'info' => '',
  'type' => 'collection',
  'fields' => [
    0 => [
      'name' => 'name',
      'type' => 'text',
      'label' => 'Name',
      'info' => '',
      'group' => 'data',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'multiline' => false,
        'showCount' => true,
        'readonly' => false,
        'placeholder' => NULL,
        'minlength' => NULL,
        'maxlength' => NULL,
        'list' => NULL,
      ],
    ],
    1 => [
      'name' => 'adress',
      'type' => 'text',
      'label' => 'Adresse',
      'info' => '',
      'group' => 'data',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'multiline' => false,
        'showCount' => true,
        'readonly' => false,
        'placeholder' => NULL,
        'minlength' => NULL,
        'maxlength' => NULL,
        'list' => NULL,
      ],
    ],
    2 => [
      'name' => 'person',
      'type' => 'contentItemLink',
      'label' => 'Person',
      'info' => 'Zu welcher Person gehört dieser Eintrag',
      'group' => 'Referenz',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'link' => 'person',
        'filter' => NULL,
        'display' => NULL,
      ],
    ],
    3 => [
      'name' => 'from',
      'type' => 'date',
      'label' => 'Einzugsdatum',
      'info' => '',
      'group' => 'Datum',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
      ],
    ],
    4 => [
      'name' => 'to',
      'type' => 'date',
      'label' => 'Auszugsdatum',
      'info' => '',
      'group' => 'Datum',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
      ],
    ],
    5 => [
      'name' => 'type',
      'type' => 'select',
      'label' => 'Wohnart',
      'info' => '',
      'group' => 'data',
      'i18n' => false,
      'required' => false,
      'multiple' => false,
      'meta' => [
      ],
      'opts' => [
        'options' => [
          0 => 'Unterkunft',
          1 => 'Gefängnis',
          2 => 'Lager',
        ],
        'multiple' => false,
      ],
    ],
  ],
  'preview' => [
  ],
  'group' => 'Unterkunft',
  'meta' => NULL,
  '_created' => 1764673577,
  '_modified' => 1764674834,
  'color' => NULL,
  'revisions' => false,
];